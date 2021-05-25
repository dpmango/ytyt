<template>
  <div class="hero">
    <LandingHeader />

    <div class="hero__body">
      <div class="hero__container container">
        <h1 class="hero__title"><span>Понятные</span> уроки <br />программирования</h1>
        <p class="hero__subtitle">С нуля до полноценного Python-разработчика с 12 проектами в портфолио</p>
        <img src="~assets/landing/img/hero__img.svg" alt="" class="hero__img" />
        <NuxtLink to="/auth/signup" class="hero__button button">Начать бесплатно</NuxtLink>
      </div>
    </div>
  </div>
</template>

<style lang="scss" scoped>
.hero {
  background-color: $fontColor;
  color: #fff;
  padding-bottom: 252px;
  margin-bottom: 90px;
  &__container {
    position: relative;
  }
  &__title {
    padding-top: 92px;
    font-size: 48px;
    margin-bottom: 30px;
    span {
      position: relative;
      &::after {
        content: '';
        position: absolute;
        bottom: -5px;
        left: 0;
        background: url('~assets/landing/img/underline.svg') no-repeat 50% 50%;
        width: 230px;
        height: 10px;
      }
    }
  }
  &__subtitle {
    font-size: 20px;
    line-height: 1.5;
    opacity: 0.8;
    margin-bottom: 40px;
    width: 435px;
  }
  &__img {
    position: absolute;
    right: 0;
    top: 0;
    width: 59%;
  }
}
@include r($xl) {
  .hero {
    height: auto;
    padding-bottom: 180px;
    &__img {
      top: 5%;
    }
  }
}

@include r($lg) {
  .hero {
    height: auto;
    padding-bottom: 90px;
    margin-bottom: 32px;
    &__container {
      display: flex;
      flex-direction: column;
      align-items: center;
      text-align: center;
    }
    &__title {
      padding-top: 0;
    }
    &__subtitle {
      margin: 0 auto;
      margin-bottom: 30px;
    }
    &__img {
      display: none;
    }
  }
}
@include r($sm) {
  .hero {
    padding-bottom: 50px;
    &__title {
      font-size: 32px;
      margin-bottom: 24px;
      span {
        &::after {
          bottom: -8px;
          width: 145px;
        }
      }
    }
    &__subtitle {
      width: 100%;
      margin-bottom: 28px;
    }
    &__button {
      width: 100%;
    }
  }
}
</style>
