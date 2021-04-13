<template>
  <header class="header">
    <div class="container">
      <div class="header__wrapper">
        <NuxtLink to="/" class="header__logo">
          <img src="~/assets/img/logo-simple.png" srcset="~/assets/img/logo-simple@2x.png 2x" alt="logo" />
        </NuxtLink>
        <div class="header__search">
          <CourseSearch />
        </div>
        <div class="header__user">
          <NuxtLink to="/profile">
            <div class="header__user-details">{{ userEmail }}</div>
            <div class="header__user-avatar"></div>
          </NuxtLink>
        </div>
      </div>
    </div>
  </header>
</template>

<script>
import { mapGetters } from 'vuex';

export default {
  data() {
    return {
      email: null,
    };
  },
  computed: {
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
    min-width: 36px;
    min-height: 36px;
    border-radius: 50%;
    background: $colorRed;
    cursor: pointer;
  }
}
</style>
