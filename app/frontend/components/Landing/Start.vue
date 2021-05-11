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
    @media screen and (max-width: $lg) {
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
    &:hover {
      animation-name: start-shadow;
      animation-duration: 0.8s;
      animation-iteration-count: infinite;
      animation-direction: alternate;
      @media screen and (max-width: $lg) {
        animation-name: none;
      }
    }
    span {
      margin-right: 20px;
    }
    @media screen and (max-width: 1300px) {
      right: -30%;
      img {
        display: none;
      }
    }
    @media screen and (max-width: 1150px) {
      right: -40%;
    }
    @media screen and (max-width: 1060px) {
      padding-left: 15px;
      right: -50%;
    }
  }
}
@media screen and (max-width: $lg) {
  .start {
    &__row {
      flex-direction: column;
      height: auto;
    }
    &__title {
      padding: 40px 20px;
      text-align: center;
    }
    &__button {
      position: static;
      transform: translateY(30px);
      justify-content: center;
      align-items: flex-start;
      padding-top: 15px;
      padding-left: 0;
      width: 100%;
      height: 100px;
      box-shadow: 0 0 0 30px rgba($colorPrimary, 0.6), 0 0 0 20px rgba($colorPrimary, 0.7),
        0 0 0 10px rgba($colorPrimary, 0.8);
      img {
        display: block;
      }
      span {
        margin-right: 0;
      }
    }
  }
}

@media screen and (max-width: $md) {
  .start {
    &__title {
      font-size: 20px;
      padding: 15px;
    }
    &__button {
      font-size: 20px;
      transform: translateY(40px);
      img {
        display: none;
      }
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
</style>
