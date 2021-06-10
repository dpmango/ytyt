<template>
  <header class="header" @mouseleave="closeUserMenu">
    <div class="container">
      <div class="header__wrapper">
        <NuxtLink to="/course" class="header__logo">
          <img src="~/assets/img/logo-simple.png" srcset="~/assets/img/logo-simple@2x.png 2x" alt="logo" />
        </NuxtLink>
        <div class="header__search">
          <CourseSearch />
        </div>
        <div class="header__messages">
          <NuxtLink to="/messages">
            <UiSvgIcon name="envelope" />
            <div v-if="notificationDialogsCount" class="header__messages-count">
              <span>{{ notificationDialogsCount }}</span>
            </div>
          </NuxtLink>
        </div>
        <div class="header__user" @mouseenter="openUserMenu">
          <div class="header__user-avatar">
            <img :src="user.thumbnail_avatar" :alt="user.first_name" />
          </div>
          <div class="header__user-menu" :class="[userMenuOpened && 'is-opened']">
            <ul>
              <li class="header__user-name">{{ user.email }}</li>
              <li>
                <NuxtLink to="/profile">
                  <UiSvgIcon name="profile" />
                  <span>Профиль</span>
                </NuxtLink>
              </li>
              <li>
                <a @click="handleLogout">
                  <UiSvgIcon name="logout" />
                  <span>Выйти</span>
                </a>
              </li>
            </ul>
          </div>
        </div>
      </div>
    </div>
  </header>
</template>

<script>
import { mapGetters, mapActions } from 'vuex';

export default {
  data() {
    return {
      tick: 0,
      pageTitle: null,
      userMenuOpened: false,
    };
  },
  computed: {
    title(ctx) {
      return ctx.$root.$meta().refresh().metaInfo.titleChunk;
    },
    ...mapGetters('auth', ['user']),
    ...mapGetters('chat', ['notificationDialogsCount', 'notificationMessageCount']),
  },
  watch: {
    $route(newVal, oldVal) {
      this.savedPageTitle = document.querySelector('title').innerHTML;
    },
  },
  mounted() {
    this.savedPageTitle = document.querySelector('title').innerHTML;

    setInterval(() => {
      if (this.notificationMessageCount > 0) {
        if (this.tick % 2) {
          document.querySelector('title').innerHTML = this.savedPageTitle;
        } else {
          document.querySelector('title').innerHTML = `Новое сообщение (${this.notificationMessageCount})`;
        }
      } else {
        document.querySelector('title').innerHTML = this.savedPageTitle;
      }

      this.tick++;
    }, 3000);

    this.outsideClickListeners = window.addEventListener('click', this.clickOutside, false);
  },
  destroyed() {
    this.outsideClickListeners = window.removeEventListener('click', this.clickOutside, false);
  },
  methods: {
    openUserMenu() {
      this.userMenuOpened = true;
    },
    closeUserMenu() {
      this.userMenuOpened = false;
    },
    clickOutside(e) {
      if (!e.target.closest('.header__user')) {
        this.closeUserMenu();
      }
    },
    async handleLogout() {
      await this.logout()
        .then((res) => {
          this.$toast.global.default({ message: res.detail });
        })
        .catch((_err) => {});
    },
    ...mapActions('auth', ['logout']),
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
    color: $colorGray;
    transition: color 0.25s $ease;
    .svg-icon {
      font-size: 18px;
    }
    &:hover {
      color: $fontColor;
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
  &__user {
    position: relative;
    z-index: 1;
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
    transition: opacity 0.25s $ease;
    &:hover {
      opacity: 0.7;
    }
    img {
      position: absolute;
      top: 0;
      left: 0;
      width: 100%;
      height: 100%;
    }
  }
  &__user-menu {
    position: absolute;
    top: calc(100% + 10px);
    right: 0;
    min-width: 220px;
    z-index: 2;
    background: #fff;
    border-radius: 8px;
    box-shadow: 0 6px 24px -4px rgba(23, 24, 24, 0.04);
    filter: drop-shadow(0 0 12px rgba(0, 0, 0, 0.08));
    pointer-events: none;
    transform: translate(0, 10px);
    opacity: 0;
    transition: opacity 0.25s $ease, transform 0.25s $ease;
    &.is-opened {
      opacity: 1;
      transform: none;
      pointer-events: all;
    }
    ul {
      list-style: none;
      margin: 0;
      padding: 8px 0;
    }
    li {
      margin-bottom: 8px;
      display: block;
      &:last-child {
        margin-bottom: 0;
      }
    }
    a {
      padding: 8px 16px;
      display: flex;
      align-items: center;
      vertical-align: middle;
      font-size: 15px;
      cursor: pointer;
      transition: color 0.25s $ease;
      .svg-icon {
        color: $colorPrimary;
        font-size: 16px;
        margin-right: 6px;
      }
      &:hover {
        color: rgba($fontColor, 0.7);
      }
    }
  }
  &__user-name {
    font-weight: 500;
    font-size: 15px;
    padding: 8px 16px 12px;
    border-bottom: 1px solid $borderColor;
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
  }
}
</style>
