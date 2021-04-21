from rest_framework import status
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from files.api.serializers import DefaultFileSerializer


class FileUploadView(viewsets.mixins.CreateModelMixin, viewsets.GenericViewSet):

    permission_classes = (IsAuthenticated,)
    serializer_class = DefaultFileSerializer

    def create(self, request, *args, **kwargs):
        """
        Добавление файла для авторизованных пользователей.
        - Вернет полную информацию по сохраненному файлу
        - Добавление производится через form-data, где ключ для файла — это `content`
        Пример:
            curl --location --request POST 'http://localhost:8000/api/files/' \
                --header 'Authorization: JWT ....' \
                --form 'content=@"/Users/job/Desktop/Снимок экрана 2021-04-19 в 12.24.53.png"'
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        file = self.get_serializer(serializer.save()).data

        return Response(file, status=status.HTTP_201_CREATED)

    def get_serializer_context(self):
        return {
            **super().get_serializer_context(),
            'user': self.request.user,
        }
