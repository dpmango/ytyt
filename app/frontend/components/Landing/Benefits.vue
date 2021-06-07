<template>
  <section class="benefits">
    <h2 class="visually-hidden">Выгоды</h2>
    <div class="benefits__container container">
      <div class="benefits__item item-benefit">
        <span class="item-benefit__value">12</span>
        <h3 class="item-benefit__title">полноценных проектов <br />в портфолио по итогу обучения</h3>
      </div>
      <div class="benefits__item item-benefit">
        <span class="item-benefit__value">60 000+</span>
        <h3 class="item-benefit__title">строк кода</h3>
      </div>
      <div class="benefits__sticker">
        <p>Каждый проект вручную проверяется ревьюером. <b>Вы получаете подробную обратную связь.</b></p>
      </div>
    </div>
  </section>
</template>

<style lang="scss" scoped>
.benefits {
  margin-bottom: 90px;
  @include r(1210) {
    margin-bottom: 0;
  }
  &__container {
    display: flex;
    justify-content: space-between;
  }

  &__item {
    flex: 0 0 30%;
  }

  &__sticker {
    position: relative;
    flex: 0 0 37.5%;
    margin-left: auto;
    background-color: $colorRed;
    color: #fff;
    display: flex;
    align-items: center;
    padding: 40px;
    &::after {
      content: '';
      position: absolute;
      right: -200%;
      top: 0;
      width: 200%;
      height: 100%;
      background-color: $colorRed;
    }
    p {
      font-size: 20px;
      line-height: 1.5;
    }
    @include r($sm) {
      padding: 20px 0;
      p {
        font-size: 18px;
      }
    }
  }
  @include r(1210) {
    &__container {
      flex-wrap: wrap;
      justify-content: center;
    }
    &__item {
      flex: 0 0 50%;
      margin-bottom: 50px;
    }
    &__sticker {
      flex: 0 0 100%;
      justify-content: center;
      &::before {
        content: '';
        position: absolute;
        left: -200%;
        width: 200%;
        height: 100%;
        background-color: $colorRed;
      }
    }
  }
  @include r($sm) {
    &__item {
      flex: 0 0 100%;
    }
  }
}
.item-benefit {
  &__value {
    display: block;
    color: $colorRed;
    font-size: 90px;
    @include r($md) {
      font-size: 65px;
    }
  }

  &__title {
    font-size: 20px;
    line-height: 1.5;
    font-weight: normal;
  }
}
</style>
