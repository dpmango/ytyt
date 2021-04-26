from rest_framework import viewsets, status

from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny


class PaymentViewSet(viewsets.GenericViewSet):

    permission_classes = (AllowAny, )

    @action(methods=['POST'], detail=False, url_path='statuses')
    def statuses(self, request, *args, **kwargs):
        """
        Метод получает статусы по оплате в банке
        """
        print(request.data)
        return Response({'status': 'ok'}, status=status.HTTP_200_OK)

    def get_serializer_context(self):
        return {
            **super().get_serializer_context(),
            'user': self.request.user,
        }
