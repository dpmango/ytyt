<template>
  <div class="payment">
    <div class="container">
      <div class="payment__wrapper">
        <PaymentSelect />
      </div>
    </div>
    <!-- <UiButton @click="$vfm.show('paymentModal')"> Открыть </UiButton> -->
  </div>
</template>

<script>
export default {};
</script>

<style lang="scss" scoped>
.payment {
  margin: 30px 0;
  &__wrapper {
    position: relative;
    z-index: 1;
    overflow: hidden;
    max-width: 880px;
    background: #fff;
    box-shadow: 0 8px 26px -2px rgba(23, 24, 24, 0.18);
    border-radius: 8px;
    margin: 0 auto;
  }
}
</style>
