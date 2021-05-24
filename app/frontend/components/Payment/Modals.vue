<template>
  <div class="payment-modals">
    <UiModal v-model="paymentModal" name="paymentModal">
      <PaymentSelect />
    </UiModal>
  </div>
</template>

<script>
export default {
  data() {
    return {
      paymentModal: false,
    };
  },
  methods: {
    // modalClosed() {
    // },
  },
};
</script>
