<template>
  <div class="head">
    <div class="head__wrapper">
      <div class="head__back" @click="clickBack">
        <UiSvgIcon name="arrow-left" />
      </div>
      <div class="head__avatar">
        <div class="head__avatar-image">
          <img :src="data.avatar" :alt="data.name" />
        </div>
      </div>
      <div class="head__content">
        <div class="head__title">{{ data.name }}</div>
        <div class="head__status" :class="[data.status === 1 && 'is-online']">{{ status }}</div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  props: {
    data: Object,
    clickBack: Function,
  },
  computed: {
    status() {
      return this.data.status === 1 ? 'Онлайн' : 'Оффлайн';
    },
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
  &__back {
    display: none;
    flex: 0 0 30px;
    position: relative;
    min-width: 30px;
    min-height: 30px;
    margin-right: 6px;
    font-size: 0;
    color: $colorPrimary;
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
