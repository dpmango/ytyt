from django.http import HttpResponse
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from api.mixins import FlexibleSerializerModelViewSetMixin, PermissionsByActionModelViewSetMixin
from payment.api.serializers import InitCreationSerializer, InitCreditCreationSerializer
from payment.layout.tinkoff import PaymentLayout
from payment.layout.tinkoff_credit import PaymentCreditLayout
from payment.models import Payment


class PaymentViewSet(PermissionsByActionModelViewSetMixin,
                     FlexibleSerializerModelViewSetMixin,
                     viewsets.GenericViewSet):

    queryset = Payment.objects.all()

    permission_classes = (IsAuthenticated, )
    permission_classes_by_action = {
        'statuses': (AllowAny, ),
        'statuses_installment': (AllowAny, ),
    }

    serializers = {
        'init': InitCreationSerializer,
        'init_credit': InitCreditCreationSerializer,
    }

    @action(methods=['POST', 'PUT', 'GET'], detail=False, url_path='statuses')
    def statuses(self, request, *args, **kwargs):
        """
        Метод получает статусы по оплате в банке
        """
        if self.request.method in ('POST', 'PUT',):
            PaymentLayout().receive(request.data)
        return HttpResponse('OK', status=status.HTTP_200_OK, content_type='text')

    @action(methods=['POST', 'PUT', 'GET'], detail=False, url_path='statuses-installment')
    def statuses_installment(self, request, *args, **kwargs):
        """
        Метод получает статусы по оплате в банке
        """
        if self.request.method in ('POST', 'PUT',):
            PaymentCreditLayout().receive(request.data)
        return HttpResponse('OK', status=status.HTTP_200_OK, content_type='text')

    # Для особенных ХАКЕРОВ метод назван как рассрочка, чтоб не доматались
    @action(methods=['POST'], detail=False, url_path='init-installment')
    def init_credit(self, request, *args, **kwargs):
        """
        Метод инициализирует форму заполенния на получения рассрочки
        Пример ответа:
            {
                'url': 'https://forma.tinkoff.ru/docs/credit/examples/'
            }
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        payment_credit = serializer.save()

        payment_credit_layout = PaymentCreditLayout()

        url = payment_credit_layout.create(payment_credit)
        payment_credit_layout.is_valid(raise_exception=True)

        return Response({'url': url}, status=status.HTTP_200_OK)

    @action(methods=['POST'], detail=False)
    def init(self, request, *args, **kwargs):
        """
        Метод инициализирует оплату и возвращает ссылку на кассу
        Пример ответа:
            {
                'url': 'https://securepay.tinkoff.ru/rest/Authorize/1B63Y1'
            }
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        payment = serializer.save()

        payment_layout = PaymentLayout()

        url = payment_layout.init(payment)
        payment_layout.is_valid(raise_exception=True)

        return Response({'url': url}, status=status.HTTP_200_OK)

    def get_serializer_context(self):
        return {
            **super().get_serializer_context(),
            'user': self.request.user,
        }
