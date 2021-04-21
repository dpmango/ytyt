from rest_framework import serializers

from dialogs.models import Dialog, DialogMessage
from users.serializers import UserDetailSerializer
from files.api.serializers import DefaultFileSerializer


class DefaultDialogMessageSerializers(serializers.ModelSerializer):
    user = UserDetailSerializer()
    body = serializers.SerializerMethodField()
    file = DefaultFileSerializer()

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
