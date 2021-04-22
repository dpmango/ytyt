from rest_framework import serializers, exceptions

from dialogs.models import Dialog, DialogMessage
from files.api.serializers import DefaultFileSerializer
from users.models import User
from users.serializers import UserDetailSerializer


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
    user = UserDetailSerializer()
    body = serializers.SerializerMethodField()
    file = DefaultFileSerializer(required=False)

    @staticmethod
    def get_body(obj: DialogMessage):
        return obj.get_text_body()

    class Meta:
        model = DialogMessage
        fields = '__all__'


class DialogWithLastMessageSerializers(serializers.ModelSerializer):
    last_message = serializers.SerializerMethodField()

    def get_last_message(self, obj: Dialog):
        message = obj.dialogmessage_set.all().first()
        return DefaultDialogMessageSerializers(message, context=self.context).data

    class Meta:
        model = Dialog
        fields = ('id', 'last_message', )
