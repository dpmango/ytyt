<template>
  <section class="start">
    <h2 class="visually-hidden">Начни обучение</h2>
    <div class="container">
      <div class="start__row">
        <p class="start__title">Обучение еще никогда не было таким простым</p>
        <NuxtLink to="/auth/signup" class="start__button">
          <span>Начать бесплатно</span>
          <img src="~assets/landing/img/arrow-long.svg" alt="" />
        </NuxtLink>
        <NuxtLink to="/auth/signup" class="button start__button--mobile">Начать бесплатно </NuxtLink>
      </div>
    </div>
  </section>
</template>

<style lang="scss" scoped>
.start {
  margin-bottom: -50px;
  &__row {
    position: relative;
    display: flex;
    align-items: center;
    justify-content: space-between;
    overflow: hidden;
    background-color: #fff;
    box-shadow: 0 6px 24px 0 rgba(0, 0, 0, 0.1);
    padding: 36px 0;
    border-radius: 8px;
    @include r($lg) {
      padding: 0;
    }
  }

  &__title {
    font-size: 26px;
    padding-left: 40px;
    padding-right: 50%;
    font-weight: bold;
  }

  &__button {
    position: absolute;
    top: 50%;
    right: -18%;
    transform: translateY(-50%);
    background-color: $colorPrimary;
    color: #fff;
    display: flex;
    align-items: center;
    border-radius: 50%;
    height: 596px;
    width: 750px;
    font-size: 26px;
    font-weight: 500;
    padding-left: 28px;
    box-shadow: 0 0 0 72px rgba($colorPrimary, 0.6), 0 0 0 48px rgba($colorPrimary, 0.7),
      0 0 0 24px rgba($colorPrimary, 0.8);
    animation-name: end-shadow;
    animation-duration: 0.8s;
    animation-direction: alternate;
    animation-fill-mode: both;
    &:hover {
      animation-name: start-shadow;
      animation-iteration-count: infinite;
      @include r($lg) {
        animation-name: none;
      }
    }
    &--mobile {
      display: none;
    }
    span {
      margin-right: 20px;
    }
    @include r(1300) {
      right: -30%;
      img {
        display: none;
      }
    }
    @include r(1150) {
      right: -40%;
    }
    @include r(1060) {
      padding-left: 15px;
      right: -50%;
    }
  }
}
@include r($lg) {
  .start {
    &__row {
      flex-direction: column;
      height: auto;
      padding-left: 20px;
      padding-right: 20px;
    }
    &__title {
      padding: 40px 0 16px 0;
      text-align: center;
    }
    &__button {
      display: none;
    }
    &__button--mobile {
      width: 100%;
      display: inline-flex;
      max-width: 294px;
      margin-bottom: 16px;
      // height: 54px;
    }
  }
}

@include r($md) {
  .start {
    &__title {
      font-size: 20px;
      padding: 15px;
    }
  }
}

@keyframes start-shadow {
  0% {
    box-shadow: 0 0 0 72px rgba($colorPrimary, 0.6), 0 0 0 48px rgba($colorPrimary, 0.7),
      0 0 0 24px rgba($colorPrimary, 0.8);
  }
  100% {
    box-shadow: 0 0 0 78px rgba($colorPrimary, 0.4), 0 0 0 54px rgba($colorPrimary, 0.5),
      0 0 0 30px rgba($colorPrimary, 0.6);
  }
}

@keyframes end-shadow {
  0% {
    box-shadow: 0 0 0 78px rgba($colorPrimary, 0.4), 0 0 0 54px rgba($colorPrimary, 0.5),
      0 0 0 30px rgba($colorPrimary, 0.6);
  }
  100% {
    box-shadow: 0 0 0 72px rgba($colorPrimary, 0.6), 0 0 0 48px rgba($colorPrimary, 0.7),
      0 0 0 24px rgba($colorPrimary, 0.8);
  }
}
</style>
