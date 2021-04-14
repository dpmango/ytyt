<template>
  <header class="header">
    <div class="container container--wide">
      <div class="header__wrapper">
        <NuxtLink to="/" class="header__logo">
          <img src="~/assets/img/logo-simple.png" srcset="~/assets/img/logo-simple@2x.png 2x" alt="logo" />
        </NuxtLink>
        <div class="header__search">
          <CourseSearch />
        </div>
        <div class="header__messages">
          <NuxtLink to="/messages">
            <UiSvgIcon name="envelope" />
            <div class="header__messages-count">
              <span>{{ 12 }}</span>
            </div>
          </NuxtLink>
        </div>
        <div class="header__user">
          <NuxtLink to="/profile">
            <div class="header__user-details">{{ userEmail }}</div>
            <div class="header__user-avatar">
              <img :src="userAvatar" :alt="userEmail" />
            </div>
          </NuxtLink>
        </div>
      </div>
    </div>
  </header>
</template>

<script>
import { mapGetters } from 'vuex';

export default {
  computed: {
    userAvatar() {
      return this.user().avatar;
    },
    userEmail() {
      // TODO - getter as function ?
      return this.user().email;
    },
  },
  methods: {
    ...mapGetters('auth', ['user']),
  },
};
</script>

<style lang="scss" scoped>
.header {
  position: fixed;
  z-index: 99;
  top: 0;
  left: 0;
  right: 0;
  background: #fff;
  box-shadow: 0 0 20px -4px rgba(23, 24, 24, 0.08);
  &__wrapper {
    display: flex;
    align-items: center;
    padding: 10px 0;
  }
  &__logo {
    font-size: 0;
  }
  &__search {
    flex: 1 1 auto;
    padding: 0 28px;
  }
  &__messages {
    position: relative;
    padding-right: 12px;
    padding-top: 7px;
    margin-right: 24px;
    .svg-icon {
      font-size: 18px;
      color: $colorGray;
    }
  }
  &__messages-count {
    position: absolute;
    top: 0;
    right: 0;
    z-index: 2;
    width: 20px;
    height: 20px;
    display: flex;
    align-items: center;
    justify-content: center;
    text-align: center;
    border-radius: 50%;
    background: $colorRed;
    color: white;
    span {
      font-size: 12px;
    }
  }
  &__user a {
    display: flex;
    align-items: center;
    transition: opacity 0.25s $ease;
    &:hover {
      opacity: 0.7;
    }
  }
  &__user-details {
    padding-right: 10px;
    font-size: 12px;
  }
  &__user-avatar {
    position: relative;
    z-index: 1;
    min-width: 36px;
    min-height: 36px;
    border-radius: 50%;
    background: $colorGray;
    cursor: pointer;
    overflow: hidden;
    img {
      position: absolute;
      top: 0;
      left: 0;
      width: 100%;
      height: 100%;
    }
  }
}

@include r($md) {
  .header {
    &__logo {
      order: 1;
    }
    &__search {
      flex: 0 0 40px;
      order: 3;
      padding: 0;
      margin-right: 12px;
    }
    &__messages {
      order: 2;
      margin-right: 12px;
      margin-left: auto;
    }
    &__user {
      order: 4;
    }
    &__user-details {
      display: none;
    }
  }
}
</style>
