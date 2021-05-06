<template>
  <div class="test">
    <PaymentSelect />
    <UiModal v-model="paymentModal" name="paymentModal">
      <PaymentSelect />
    </UiModal>
    <UiButton @click="$vfm.show('paymentModal')"> Открыть </UiButton>
  </div>
</template>

<script>
export default {
  data() {
    return {
      paymentModal: false,
    };
  },
  head: {
    title: 'Оплата',
  },
};
</script>
