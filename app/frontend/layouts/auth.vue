<template>
  <div class="page">
    <div class="page__content">
      <div class="auth">
        <div class="container">
          <div class="auth__wrapper">
            <div class="auth__logo">
              <img src="~/assets/img/logo.png" srcset="~/assets/img/logo@2x.png 2x" alt="logo" />
            </div>
            <div class="auth__box">
              <Nuxt />
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  middleware: ['auth'],
};
</script>

<style lang="scss" scoped>
.auth {
  &__wrapper {
    width: 100%;
    max-width: 522px;
    margin: 0 auto;
    padding: 44px 0;
  }
  &__logo {
    color: $colorGreen;
    font-size: 0;
    text-align: center;
  }
  &__box {
    margin-top: 44px;
    background: #fff;
    border-radius: 8px;
  }
}

@include r($sm) {
  .auth {
    background: white;
    &__wrapper {
      width: 100%;
      max-width: 100%;
      padding: 40px 0;
      height: 100vh;
      max-height: 720px;
      display: flex;
      flex-direction: column;
    }
    &__logo {
      flex: 0 0 auto;
    }
    &__box {
      flex: 1 0 auto;
      display: flex;
      flex-direction: column;
      background: transparent;
      border-radius: 0;
      margin-top: 40px;
    }
  }
}
</style>
