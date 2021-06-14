<template>
  <div class="head">
    <div class="head__wrapper">
      <div v-if="clickBack" class="head__back" @click="clickBack">
        <UiSvgIcon name="arrow-left" />
      </div>
      <div class="head__avatar">
        <div class="head__avatar-image">
          <img :src="head.thumbnail_avatar" :alt="head.first_name" />
        </div>
      </div>
      <div class="head__content">
        <div class="head__title">
          {{ title }} <span v-if="user.is_support">({{ head.email }})</span>
        </div>
        <div class="head__status" :class="[head.status_online && 'is-online']">{{ status }}</div>
      </div>
      <div v-if="clickBackMini" class="head__mini-close" @click="clickBackMini">
        <UiSvgIcon name="close" />
      </div>
    </div>
  </div>
</template>

<script>
import { mapGetters } from 'vuex';

export default {
  props: {
    head: Object,
    clickBack: Function,
    clickBackMini: Function,
  },
  computed: {
    title() {
      const { first_name, last_name, email } = this.head;

      if (first_name) {
        return `${first_name} ${last_name}`;
      } else {
        return email;
      }
    },
    status() {
      return this.head.status_online ? 'Онлайн' : 'Оффлайн';
    },
    ...mapGetters('auth', ['user']),
  },
};
</script>

<style lang="scss" scoped>
.head {
  border-bottom: 1px solid rgba(147, 149, 152, 0.2);
  padding: 16px;
  &__wrapper {
    display: flex;
  }
  &__back,
  &__mini-close {
    flex: 0 0 30px;
    position: relative;
    min-width: 30px;
    min-height: 30px;
    font-size: 0;
    cursor: pointer;
    transition: color 0.25s $ease;
    .svg-icon {
      position: absolute;
      top: 50%;
      left: 50%;
      transform: translate(-50%, -50%);
      font-size: 18px;
    }
    &:hover {
      color: $fontColor;
    }
  }
  &__back {
    display: none;
    margin-right: 6px;
    color: $colorPrimary;
  }
  &__mini-close {
    align-self: center;
    margin-left: 6px;
    color: rgba($fontColor, 0.5);
  }
  &__avatar {
    flex: 0 0 44px;
    max-width: 44px;
  }
  &__avatar-image {
    position: relative;
    z-index: 1;
    width: 44px;
    height: 44px;
    border-radius: 50%;
    background: $colorGray;
    overflow: hidden;
    img {
      position: absolute;
      top: 0;
      left: 0;
      width: 100%;
      height: 100%;
      object-fit: contain;
    }
  }

  &__content {
    flex: 1 1 auto;
    max-width: 100%;
    padding-left: 12px;
  }
  &__title {
    font-weight: 500;
    font-size: 15px;
    margin-right: 6px;
    span {
      color: $colorGray;
    }
  }
  &__status {
    font-size: 14px;
    color: $colorGray;
    transition: color 0.25s $ease;
    &.is-online {
      color: $colorPrimary;
    }
  }
}

@include r($md) {
  .head {
    &__back {
      display: block;
    }
  }
}
</style>
