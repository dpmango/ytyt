<template>
  <div class="error">
    <div class="container">
      <div class="error__wrapper">
        <div class="error__content">
          <template v-if="error.statusCode === 404">
            <div class="error__title">404</div>
            <div class="error__description">Упс, кажется вы потерялись</div>
          </template>
          <template v-else>
            <div class="error__title">Неизвестная ошибка</div>
            <div class="error__description">Попробуйте еще раз</div>
          </template>

          <div class="error__cta">
            <NuxtLink to="/course">
              <UiButton theme="primary">Вернуться на главную</UiButton>
            </NuxtLink>
          </div>
        </div>

        <div class="error__image">
          <img src="~/assets/img/404.svg" alt="logo" />
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  props: {
    error: Object,
  },
  mouted() {
    // eslint-disable-next-line no-console
    console.log(this.error);
  },
};
</script>

<style lang="scss">
.error {
  &__wrapper {
    position: relative;
    padding: 32px 0 128px;
    min-height: calc(100vh - 57px);
    display: flex;
    flex-direction: column;
  }
  &__content {
    position: relative;
    z-index: 2;
    text-align: center;
    margin: auto 0;
  }
  &__title {
    font-weight: 500;
    font-size: 72px;
    line-height: 1.3;
  }
  &__description {
    font-size: 20px;
  }
  &__cta {
    margin-top: 40px;
  }
  &__image {
    position: absolute;
    z-index: 1;
    bottom: 0;
    left: 0;
    font-size: 0;
    img {
      max-width: 100%;
    }
  }
}

@include r($md) {
  .error {
    &__wrapper {
      min-height: 1px;
      padding: 48px 0 0;
    }
    &__image {
      margin-top: 42px;
      position: relative;
      // text-align: center;
    }
  }
}
</style>
