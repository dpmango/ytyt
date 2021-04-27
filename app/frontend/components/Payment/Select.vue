<template>
  <div class="payment">
    <div class="container">
      <div class="payment__wrapper">
        <h1 class="payment__title">Выберите способ оплаты</h1>
        <div class="row payment__list">
          <div class="col col-4 col-md-12">
            <div class="card">
              <div class="card__name">Оплатить сразу</div>
              <div class="card__price">
                <span class="card__price-val">54 000</span>
                <span class="card__price-help">₽</span>
              </div>
              <div class="card__desc">Без скидки 60 000 ₽</div>
            </div>
          </div>
          <div class="col col-4 col-md-12">
            <div class="card">
              <div class="card__name">Рассрочка на 6 мес.</div>
              <div class="card__price">
                <span class="card__price-val">10 000</span>
                <span class="card__price-help">₽<span>/мес</span></span>
              </div>
              <div class="card__desc">Суммарно 60 000 ₽</div>
            </div>
          </div>
          <div class="col col-4 col-md-12">
            <div class="card">
              <div class="card__name">Рассрочка на 12 мес.</div>
              <div class="card__price">
                <span class="card__price-val">5 000</span>
                <span class="card__price-help">₽<span>/мес</span></span>
              </div>
              <div class="card__desc">Суммарно 60 000 ₽</div>
            </div>
          </div>
        </div>
        <div class="payment__partner">Рассрочка предоставляется банком Тинькофф</div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  methods: {
    // modalClosed() {
    // },
  },
};
</script>

<style lang="scss" scoped>
.payment {
  margin: 32px 0;
  &__wrapper {
    max-width: 684px;
    margin: 0 auto;
  }
  &__title {
    font-weight: 500;
    font-size: 28px;
    text-align: center;
  }
  &__list {
    margin: 22px -6px -6px;
    .col {
      padding: 6px;
    }
  }
  &__partner {
    margin-top: 28px;
    font-size: 15px;
    text-align: center;
    opacity: 0.5;
  }
}

.card {
  padding: 20px 8px 24px;
  background: #fff;
  box-shadow: 0 6px 24px -4px rgba(23, 24, 24, 0.1);
  border-radius: 8px;
  text-align: center;
  cursor: pointer;
  transition: box-shadow 0.25s $ease;
  &:hover {
    box-shadow: 0 8px 26px -2px rgba(23, 24, 24, 0.18);
  }
  &__name {
    font-weight: 500;
    font-size: 17px;
  }
  &__price {
    margin-top: 4px;
    font-size: 28px;
  }
  // &__price-val{
  // }
  &__price-help {
    opacity: 0.5;
    span {
      font-size: 17px;
    }
  }
  &__desc {
    margin-top: 4px;
    font-size: 15px;
    opacity: 0.5;
  }
}
</style>
