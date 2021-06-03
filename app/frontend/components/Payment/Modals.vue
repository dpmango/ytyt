<template>
  <div class="payment-modals">
    <UiModal v-model="paymentStart" name="paymentStart" content-class="narrow">
      <div class="payment-modals__text">
        <p>Бесплатный курс пройден, произведите оплату для продолжения обучения</p>
      </div>

      <div class="payment-modals__cta">
        <UiButton theme="outline" @click="$vfm.hide('paymentStart')">Отмена</UiButton>
        <UiButton @click="$vfm.show('paymentModal')">Перейти к оплате</UiButton>
      </div>
    </UiModal>

    <UiModal v-model="paymentModal" name="paymentModal">
      <PaymentSelect />
    </UiModal>
  </div>
</template>

<script>
export default {
  data() {
    return {
      paymentStart: false,
      paymentModal: false,
    };
  },
  methods: {
    // modalClosed() {
    // },
  },
};
</script>

<style lang="scss" scoped>
.payment-modals {
  &__text {
    text-align: center;
    font-size: 19px;
    p {
      margin: 0;
      + p {
        margin-top: 1em;
      }
    }
  }
  &__cta {
    display: flex;
    align-items: center;
    justify-content: center;
    margin-top: 24px;
    .button {
      padding-top: 14px;
      padding-bottom: 13px;
      margin-right: 12px;
      &:last-child {
        margin-right: 0;
      }
    }
  }
}
</style>
