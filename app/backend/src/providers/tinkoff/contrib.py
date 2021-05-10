import json

from django.conf import settings
from loguru import logger
from requests import request, Response
from hashlib import sha256


class Tinkoff:
    PAYMENT_METHOD_FULL_PAYMENT = 'full_payment'
    PAYMENT_METHOD_FULL_PREPAYMENT = 'full_prepayment'
    PAYMENT_METHOD_PREPAYMENT = 'prepayment'
    PAYMENT_METHOD_ADVANCE = 'advance'
    PAYMENT_METHOD_PARTIAL_PAYMENT = 'partial_payment'
    PAYMENT_METHOD_CREDIT = 'credit'
    PAYMENT_METHOD_CREDIT_PAYMENT = 'credit_payment'
    PAYMENT_METHODS = (
        (PAYMENT_METHOD_FULL_PAYMENT, 'Полный расчет'),
        (PAYMENT_METHOD_FULL_PREPAYMENT, 'Предоплата 100%'),
        (PAYMENT_METHOD_PREPAYMENT, 'Предоплата'),
        (PAYMENT_METHOD_ADVANCE, 'Аванс'),
        (PAYMENT_METHOD_PARTIAL_PAYMENT, 'Частичный расчет и кредит'),
        (PAYMENT_METHOD_CREDIT, 'Передача в кредит'),
        (PAYMENT_METHOD_CREDIT_PAYMENT, 'Оплата кредита'),

    )

    TAX_NONE = 'none'
    TAX_VAT0 = 'vat0'
    TAX_VAT10 = 'vat10'
    TAX_VAT20 = 'vat20'
    TAX_VAT110 = 'vat110'
    TAX_VAT120 = 'vat120'
    TAXES = (
        (TAX_NONE, 'Без НДС'),
        (TAX_VAT0, '0%'),
        (TAX_VAT10, '10%'),
        (TAX_VAT20, '20%'),
        (TAX_VAT110, '10/110'),
        (TAX_VAT120, '20/120'),
    )

    TAXATION_OSN = 'osn'
    TAXATION_USN_INCOME = 'usn_income'
    TAXATION_USN_INCOME_OUTCOME = 'usn_income_outcome'
    TAXATION_PATENT = 'patent'
    TAXATION_ENVD = 'envd'
    TAXATION_ESN = 'esn'
    TAXATIONS = (
        (TAXATION_OSN, 'Общая'),
        (TAXATION_USN_INCOME, 'Упрощенная (доходы)'),
        (TAXATION_USN_INCOME_OUTCOME, 'Упрощенная (доходы минус расходы)'),
        (TAXATION_PATENT, 'Патентная'),
        (TAXATION_ENVD, 'Единый налог на вмененный доход'),
        (TAXATION_ESN, 'Единый сельскохозяйственный налог'),
    )

    STATUS_NEW = 'NEW'
    STATUS_FORM_SHOWED = 'FORM_SHOWED'
    STATUS_DEADLINE_EXPIRED = 'DEADLINE_EXPIRED'
    STATUS_CANCELED = 'CANCELED'
    STATUS_PREAUTHORIZING = 'PREAUTHORIZING'
    STATUS_AUTHORIZING = 'AUTHORIZING'
    STATUS_AUTHORIZED = 'AUTHORIZED'
    STATUS_AUTH_FAIL = 'AUTH_FAIL'
    STATUS_REJECTED = 'REJECTED'
    STATUS_3DS_CHECKING = '3DS_CHECKING'
    STATUS_3DS_CHECKED = '3DS_CHECKED'
    STATUS_REVERSING = 'REVERSING'
    STATUS_PARTIAL_REVERSED = 'PARTIAL_REVERSED'
    STATUS_REVERSED = 'REVERSED'
    STATUS_CONFIRMING = 'CONFIRMING'
    STATUS_CONFIRMED = 'CONFIRMED'
    STATUS_REFUNDING = 'REFUNDING'
    STATUS_PARTIAL_REFUNDED = 'PARTIAL_REFUNDED'
    STATUS_REFUNDED = 'REFUNDED'
    STATUSES = (
        (STATUS_NEW, 'Создан'),
        (STATUS_FORM_SHOWED, 'Платежная форма открыта покупателем'),
        (STATUS_DEADLINE_EXPIRED, 'Просрочен'),
        (STATUS_CANCELED, 'Отменен'),
        (STATUS_PREAUTHORIZING, 'Проверка платежных данных'),
        (STATUS_AUTHORIZING, 'Резервируется'),
        (STATUS_AUTHORIZED, 'Зарезервирован'),
        (STATUS_AUTH_FAIL, 'Не прошел авторизацию'),
        (STATUS_REJECTED, 'Отклонен'),
        (STATUS_3DS_CHECKING, 'Проверяется по протоколу 3-D Secure'),
        (STATUS_3DS_CHECKED, 'Проверен по протоколу 3-D Secure'),
        (STATUS_REVERSING, 'Резервирование отменяется'),
        (STATUS_PARTIAL_REVERSED, 'Резервирование отменено частично'),
        (STATUS_REVERSED, 'Резервирование отменено'),
        (STATUS_CONFIRMING, 'Подтверждается'),
        (STATUS_CONFIRMED, 'Подтвержден'),
        (STATUS_REFUNDING, 'Возвращается'),
        (STATUS_PARTIAL_REFUNDED, 'Возвращен частично'),
        (STATUS_REFUNDED, 'Возвращен полностью'),
    )

    def __init__(self, base_url: str, terminal_key: str, terminal_password: str, admin_email: str):
        self.base_url = base_url
        self.terminal_key = terminal_key
        self.terminal_password = terminal_password
        self.admin_email = admin_email

    def init(self, **kwargs):
        """
        Метод создает платеж: продавец получает ссылку на платежную форму и должен перенаправить по ней покупателя
        """
        data = {'TerminalKey': self.terminal_key, **kwargs}
        return self._call('post', url='Init', json=data)

    def confirm(self, **kwargs):
        """
        Метод подтверждает платеж и списывает ранее заблокированные средства.

        Используется при двухстадийной оплате. При одностадийной оплате вызывается автоматически. Применим к платежу
        только в статусе AUTHORIZED и только один раз.

        Сумма подтверждения не может быть больше заблокированной. Если сумма подтверждения меньше заблокированной,
        будет выполнено частичное подтверждение.
        """
        data = {'TerminalKey': self.terminal_key, **kwargs}
        data.update({'Token': self._create_signature(**data)})

        return self._call('post', url='Confirm', json=data)

    def _create_signature(self, **kwargs):
        """
        Подпись подтверждения оплаты
        Описние алгоритма — https://www.tinkoff.ru/kassa/develop/api/request-sign/
        :param kwargs: Аргументы на основе которых будет выполнено хеширование
        """
        to_hash = [{key: value} for key, value in kwargs.items()]
        to_hash.append({'Password': self.terminal_password})

        to_hash = sorted(to_hash, key=lambda item: list(item.keys())[0])
        to_hash = ''.join([str(list(item.values())[0]) for item in to_hash])

        return sha256(to_hash.encode('utf-8')).hexdigest()

    def _call(self, method: str, url: str, **kwargs):
        """
        Вызов необходимого метода API из url
        :param method: Метод для запроса
        :param url: url api-метода
        :param kwargs: Аргументы для вызова
        """
        base_url = self.base_url.rstrip('/')
        url = '%s/%s' % (base_url, url)

        logger.debug('[tinkoff][request][method=%s] url=%s, kwargs=%s' % (method, url, str(kwargs)))
        response = request(method=method, url=url, **kwargs, headers={'content-type': 'application/json'})

        if response.status_code in (200, 201, 202):
            return self._force_json(response)

        logger.info('[tinkoff][response][method=%s] status_code=%s, url=%s, response=%s' % (
            method, response.status_code, url, str(response.text)
        ))
        return {}

    @staticmethod
    def _force_json(response: Response):
        try:
            return response.json()
        except json.JSONDecodeError:
            return {}


tinkoff_client = Tinkoff(
    base_url=settings.TINKOFF_URL,
    terminal_key=settings.TINKOFF_TERMINAL_KEY,
    terminal_password=settings.TINKOFF_TERMINAL_PASSWORD,
    admin_email=settings.DEFAULT_ADMIN_EMAIL,
)
