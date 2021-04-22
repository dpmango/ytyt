from rest_framework import viewsets, status

from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from dialogs.api.serializers import CreateDialogMessageSerializers


class DialogViewSet(viewsets.GenericViewSet):

    permission_classes = (IsAuthenticated, )
    serializer_class = CreateDialogMessageSerializers

    @action(methods=['POST'], detail=False, url_path='new-message')
    def create_new_message(self, request, *args, **kwargs):
        """
        Отправка нового сообщения ревьюеру
        Если диалога с ревьюером ранее не было, то он будет создан
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def get_serializer_context(self):
        return {
            **super().get_serializer_context(),
            'user': self.request.user,
        }
