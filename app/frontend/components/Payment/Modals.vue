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

    <UiModal v-model="paymentStart2" name="paymentStart2" content-class="narrow">
      <div class="payment-modals__text">
        <p>Пока что вам доступен только бесплатный курс, для получения полного доступа требуется оплата</p>
      </div>

      <div class="payment-modals__cta">
        <UiButton theme="outline" @click="$vfm.hide('paymentStart2')">Отмена</UiButton>
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
  computed: {
    paymentStart: {
      get() {
        return this.$store.state.ui.modalPaymentStart;
      },
      set(value) {
        this.$store.commit('ui/setModalPaymentStart', value);
      },
    },
    paymentStart2: {
      get() {
        return this.$store.state.ui.modalPaymentStart2;
      },
      set(value) {
        this.$store.commit('ui/setModalPaymentStart2', value);
      },
    },
    paymentModal: {
      get() {
        return this.$store.state.ui.modalPaymentModal;
      },
      set(value) {
        this.$store.commit('ui/setModalPaymentModal', value);
      },
    },
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

@include r($sm) {
  .payment-modals {
    &__text {
      font-size: 18px;
    }
    &__cta {
      margin-top: 20px;
      flex-direction: column-reverse;
      .button {
        margin-top: 8px;
        margin-right: 0;
        width: 100%;
        &:last-child {
          margin-top: 0;
        }
      }
    }
  }
}
</style>
