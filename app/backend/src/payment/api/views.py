from rest_framework import viewsets, status

from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated

from api.mixins import FlexibleSerializerModelViewSetMixin
from payment.models import Payment
from payment.api.serializers import InitCreationSerializer, InitInstallmentCreationSerializer
from payment.contrib import payment_layout


class PaymentViewSet(FlexibleSerializerModelViewSetMixin, viewsets.GenericViewSet):

    queryset = Payment.objects.all()

    permission_classes = (IsAuthenticated, )
    permission_classes_by_action = {
        'statuses': (AllowAny, )
    }

    serializers = {
        'init': InitCreationSerializer,
        'init_installment': InitInstallmentCreationSerializer,
    }

    @action(methods=['POST'], detail=False, url_path='statuses')
    def statuses(self, request, *args, **kwargs):
        """
        Метод получает статусы по оплате в банке
        """
        payment_layout.receive(request.data)
        return Response('ОК', status=status.HTTP_200_OK)

    @action(methods=['POST'], detail=False, url_path='init-installment')
    def init_installment(self, request, *args, **kwargs):
        """
        Метод инициализирует форму заполенния на получения рассрочки
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        payment_installment = serializer.save()

        return Response({'payment_url': 'url'}, status=status.HTTP_200_OK)

    @action(methods=['POST'], detail=False)
    def init(self, request, *args, **kwargs):
        """
        Метод инициализирует оплату и возвращает ссылку на кассу
        Пример ответа:
            {
                'payment_url': 'https://securepay.tinkoff.ru/rest/Authorize/1B63Y1'
            }
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        payment = serializer.save()

        url = payment_layout.init(payment)
        payment_layout.is_valid(raise_exception=True)

        return Response({'payment_url': url}, status=status.HTTP_200_OK)

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
