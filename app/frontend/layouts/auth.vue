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
</style>
