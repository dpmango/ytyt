<template>
  <div class="payment">
    <div class="container">
      <h1 class="h3-title">Оплатите доступ к курсам</h1>
      <div class="row payment__list">
        <div class="col payment__col">
          <div class="card">
            <div class="card__icon">
              <UiSvgIcon name="camera" />
            </div>
            <div class="card__name">Оплата картой</div>
            <div class="card__desc">Оплатите банквоской картой</div>
          </div>
        </div>
        <div class="col payment__col">
          <div class="card">
            <div class="card__icon">
              <UiSvgIcon name="camera" />
            </div>
            <div class="card__name">Рассросчка</div>
            <div class="card__desc">Оформите кредит</div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {};
</script>

<style lang="scss" scoped>
.payment {
  margin-top: 24px;
  &__list {
    margin-top: 16px;
  }
  &__col {
    flex: 0 0 300px;
    max-width: 300px;
  }
}

.card {
  border: 1px solid $borderColor;
  padding: 16px;
  border-radius: 6px;
  &__icon {
    color: $colorGray;
    font-size: 40px;
    text-align: center;
  }
  &__name {
    font-size: 17px;
    font-weight: 500;
  }
}
</style>
