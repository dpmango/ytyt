from django.conf import settings

from providers.core import BaseProvider


class TinkoffCredit(BaseProvider):

    # Съема подключения — https://forma.tinkoff.ru/docs/credit/help/scheme/

    PROMO_CODE_0_0_4 = 'installment_0_0_4_5'
    PROMO_CODE_0_0_6 = 'installment_0_0_6_6'
    PROMO_CODE_0_0_10 = 'installment_0_0_10_10'
    PROMO_CODE_0_0_12 = 'installment_0_0_12_11'

    PROMO_CODES = (
        (PROMO_CODE_0_0_4, '0-0-4'),
        (PROMO_CODE_0_0_6, '0-0-6'),
        (PROMO_CODE_0_0_10, '0-0-10'),
        (PROMO_CODE_0_0_12, '0-0-12'),
    )

    STATUS_APPROVED = 'Approved'
    STATUS_REJECTED = 'Rejected'
    STATUS_CANCELED = 'Canceled'
    STATUS_SIGNED = 'Signed'
    STATUSES = (
        (STATUS_APPROVED, 'Заявка одобрена'),
        (STATUS_REJECTED, 'По заявке отказ'),
        (STATUS_CANCELED, 'Заявка отменена'),
        (STATUS_SIGNED, 'Договор подписан'),
    )

    def __init__(self, base_url: str, shop_id: str, showcase_id: str):
        self.base_url = base_url
        self.shop_id = shop_id
        self.showcase_id = showcase_id

    def create(self, **kwargs):
        """
        Метод для создания заявки на кредит или рассрочку
        """
        data = {
            'shopId': self.shop_id,
            'showcaseId': self.showcase_id,
            **kwargs,
        }
        return self._call('post', url='orders/create', json=data)

    def create_demo(self, **kwargs):
        """
        Метод для создания демо-заявки на кредит или рассрочку
        """
        data = {**kwargs}
        return self._call('post', url='orders/create-demo', json=data)


tinkoff_client = TinkoffCredit(
    base_url=settings.TINKOFF_CREDIT_URL,
    shop_id=settings.TINKOFF_CREDIT_SHOP_ID,
    showcase_id=settings.TINKOFF_CREDIT_SHOWCASE_ID,
)
