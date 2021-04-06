from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from api.mixins import FlexibleSerializerModelViewSetMixin


class LessonFragmentViewSet(FlexibleSerializerModelViewSetMixin,
                            viewsets.GenericViewSet):

    permission_classes = (IsAuthenticated, )
    # TODO: тут сделать проверку на скорость прохождения курса


    @action(methods=['POST'], detail=True, url_path='next')
    def next(self, request, pk=None, *args, **kwargs):
        """
        Метод предоставляет доступ к следующему фрагменту урока
        """

        user = request.user



        return Response({},)

    def get_serializer_context(self):
        return {
            **super().get_serializer_context(),
            'user': self.request.user,
        }
