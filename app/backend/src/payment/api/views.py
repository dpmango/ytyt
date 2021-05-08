from rest_framework import viewsets, status

from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.decorators import api_view, permission_classes

from api.mixins import FlexibleSerializerModelViewSetMixin
from payment.models import Payment
from payment.api.serializers import InitCreationSerializer
from payment.contrib import payment_layout


class PaymentViewSet(FlexibleSerializerModelViewSetMixin, viewsets.GenericViewSet):

    queryset = Payment.objects.all()

    permission_classes = (AllowAny, )
    permission_classes_by_action = {
        'statuses': (AllowAny, )
    }

    serializers = {
        'init': InitCreationSerializer,
    }

    @action(methods=['POST'], detail=False, url_path='statuses')
    def statuses(self, request, *args, **kwargs):
        """
        Метод получает статусы по оплате в банке
        """
        print(request.data)
        return Response({'status': 'ok'}, status=status.HTTP_200_OK)

    @action(methods=['POST'], detail=False)
    def init(self, request, *args, **kwargs):

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        payment = serializer.save()

        payment_layout.init(payment)



        return Response({})






    def get_serializer_context(self):
        return {
            **super().get_serializer_context(),
            'user': self.request.user,
        }

    def get_permissions(self):
        try:
            return [permission() for permission in self.permission_classes_by_action[self.action]]
        except KeyError:
            return [permission() for permission in self.permission_classes]
