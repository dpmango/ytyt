<template>
  <div class="lesson__nav nav">
    <div class="nav__title">
      <span class="nav__title-count">{{ currentSectionIndex + 1 }}/{{ sectionsCount }}</span>
      {{ title }}
    </div>
    <div class="nav__actions">
      <a href="#" class="nav__actions-prev" :class="[!isPrevAvailable && 'disabled']" @click.prevent="setPrevLesson">
        <UiSvgIcon name="arrow-left-filled" />
        <span>Предыдущий урок</span>
      </a>
      <a href="#" class="nav__actions-next" :class="[!isNextAvailable && 'disabled']" @click.prevent="setNextLesson">
        <span>Следующий урок</span>
        <UiSvgIcon name="arrow-right-filled" />
      </a>
    </div>
  </div>
</template>

<script>
export default {
  props: {
    title: String,
    currentSectionIndex: Number,
    sectionsCount: Number,
    isPrevAvailable: Number,
    isNextAvailable: Number,
    setNextLesson: Function,
    setPrevLesson: Function,
  },
};
</script>

<style lang="scss" scoped>
.nav {
  display: flex;
  align-items: center;
  padding: 16px 20px 15px 20px;
  border-bottom: 1px solid rgba(#171818, 0.1);
  &__title {
    font-size: 15px;
  }
  &__title-count {
    color: $colorGray;
  }
  &__actions {
    margin-left: auto;
    display: flex;
    align-items: center;
    a {
      display: inline-flex;
      align-items: center;
      font-size: 15px;
      margin-right: 16px;
      color: $colorPrimary;
      cursor: pointer;
      transition: color 0.25s $ease;
      &:hover {
        color: $fontColor;
      }
      &.disabled {
        color: $colorGray;
        pointer-events: none;
      }
      &:last-child {
        margin-right: 0;
      }
    }
  }
  &__actions-prev {
    .svg-icon {
      font-size: 18px;
      margin-right: 8px;
    }
  }
  &__actions-next {
    .svg-icon {
      font-size: 18px;
      margin-left: 8px;
    }
  }
}
</style>
