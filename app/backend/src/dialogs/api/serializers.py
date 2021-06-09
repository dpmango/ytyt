import typing as t

from django.db.models import Q
from rest_framework import serializers, exceptions

from courses.api.course_lesson.serializers import CourseLessonInMessageSerializers
from dialogs.models import Dialog, DialogMessage
from files.api.serializers import DefaultFileSerializer
from users.models import User
from users.serializers import UserDialogSmallDetailSerializer


class CreateDialogMessageSerializers(serializers.Serializer):

    body = serializers.CharField(required=True)
    file_id = serializers.IntegerField(required=False)
    lesson_id = serializers.IntegerField(required=False)

    def validate_file_id(self, value: int) -> int:
        """
        Проверка прав на файл при отправке сообщения
        :param value: ID файла
        :return: ID файла
        """
        user: User = self.context.get('user')

        if not user.file_set.filter(id=value).exists():
            raise exceptions.PermissionDenied('У вас нет прав на этот файл')

        return value

    def create(self, validated_data) -> DialogMessage:
        """
        Создание сообщения со страницы с уроком
        Сообщение будет отправлено действующему ревьюеру
        Если ревьюер не назначен — будет исключение
        :param validated_data: Данные после валидации
        """
        user: User = self.context.get('user')

        reviewer = user.reviewer
        if reviewer is None:
            raise exceptions.PermissionDenied('Пользователю еще не назначен ревьюер')

        dialogs = user.dialog_users_set.all().order_by('-id')
        dialog_with_reviewer = None

        # Определяем существование диалога с ревьюером
        for dialog in dialogs:
            if reviewer in dialog.users.all():
                dialog_with_reviewer = dialog

        if dialog_with_reviewer is None:
            dialog_with_reviewer = Dialog.objects.create()
            dialog_with_reviewer.users.add(user, user.reviewer)
            dialog_with_reviewer.save()

        validated_data.update({'user_id': user.id, 'dialog_id': dialog_with_reviewer.id})
        return self.Meta.model.objects.create(**validated_data)

    def to_representation(self, instance):
        return DefaultDialogMessageSerializers(instance, context=self.context).data

    class Meta:
        model = DialogMessage


class DefaultDialogMessageSerializers(serializers.ModelSerializer):
    user = UserDialogSmallDetailSerializer()
    file = DefaultFileSerializer(required=False)
    lesson = CourseLessonInMessageSerializers(required=False)

    body = serializers.SerializerMethodField(required=False)
    text_body = serializers.SerializerMethodField(read_only=True)
    markdown_body = serializers.SerializerMethodField(required=False)

    @staticmethod
    def get_markdown_body(obj):
        return obj.body

    @staticmethod
    def get_body(obj: DialogMessage):
        if obj.body is not None:
            return obj.get_body()
        return None

    @staticmethod
    def get_text_body(obj: DialogMessage):
        if obj.body is not None:
            return obj.get_text_body()
        return None

    class Meta:
        model = DialogMessage
        exclude = ('reply', )


class DefaultDialogMessageWithReplySerializers(DefaultDialogMessageSerializers):
    reply = DefaultDialogMessageSerializers()

    class Meta:
        model = DialogMessage
        fields = '__all__'


class DialogWithLastMessageSerializers(serializers.ModelSerializer):
    unread_messages_count = serializers.SerializerMethodField()
    last_message = serializers.SerializerMethodField()
    user = serializers.SerializerMethodField()

    def get_unread_messages_count(self, obj: Dialog) -> t.Optional[int]:
        """
        Метод вернет количество непрочитанных сообщений в диалоге
        :param obj: Объект диалога
        """
        if self.context.get('user').is_support:
            return None
        return obj.dialogmessage_set.filter(~Q(user=self.context.get('user')), date_read__isnull=True).count()

    def get_user(self, obj: Dialog) -> dict:
        """
        Получение пользователя, с которым ведется диалог
        :param obj: Объект диалога
        """
        for user in obj.users.all():
            if user != self.context.get('user'):
                return UserDialogSmallDetailSerializer(user, context=self.context).data
        return {}

    def get_last_message(self, obj: Dialog):
        message = obj.dialogmessage_set.last()
        return DefaultDialogMessageSerializers(message, context=self.context).data

    class Meta:
        model = Dialog
        fields = ('id', 'unread_messages_count', 'last_message', 'user')
