<template>
  <NuxtLink
    class="card"
    :class="[theme.status === 3 && 'is-compleated', [4, 5, 6, 7, 8].includes(theme.status) && 'is-locked']"
    :to="linkHref"
  >
    <div class="card__status">
      <CoursePartStatus :status="theme.status" />
    </div>
    <div class="card__title">{{ theme.title }}</div>
    <div class="card__description">{{ theme.description }}</div>

    <div class="card__stats">
      <span>{{ stats }}</span>
    </div>
    <div class="card__progress">
      <div
        v-if="theme.count_lessons"
        class="card__progress-inner"
        :style="{ width: `${(theme.completed_count_lessons / theme.count_lessons) * 100}%` }"
      ></div>
    </div>
  </NuxtLink>
</template>

<script>
import Plurize from '~/helpers/Plurize';

export default {
  props: {
    theme: Object,
  },
  computed: {
    linkHref() {
      return this.theme.status !== 4 ? `/theme/${this.theme.id}` : '#';
    },
    stats() {
      const plural = Plurize(this.theme.count_lessons, 'урок', 'урока', 'уроков');
      return `${this.theme.completed_count_lessons} / ${this.theme.count_lessons} ${plural}`;
    },
  },
};
</script>

<style lang="scss" scoped>
.card {
  display: flex;
  flex-direction: column;
  background: #fff;
  box-shadow: 0 6px 24px -4px rgba(23, 24, 24, 0.1);
  border-radius: 8px;
  padding: 18px 16px;
  transition: box-shadow 0.25s $ease;
  &:hover {
    box-shadow: 0 8px 26px -2px rgba(23, 24, 24, 0.18);
  }
  &__title {
    margin-top: 8px;
    font-weight: 500;
    font-size: 17px;
    line-height: 1.35;
  }
  &__description {
    margin-top: 8px;
    font-size: 14px;
    opacity: 0.7;
  }
  &__stats {
    margin-top: auto;
    padding-top: 34px;
    display: flex;
    align-items: center;
    font-size: 14px;
    span {
      margin-right: 16px;
      &:last-child {
        margin-right: 0;
      }
    }
  }
  &__progress {
    position: relative;
    z-index: 1;
    margin-top: 6px;
    background: rgba(23, 24, 24, 0.08);
    border-radius: 12px;
    height: 6px;
    font-size: 0;
    overflow: hidden;
  }
  &__progress-inner {
    position: absolute;
    top: 0;
    left: 0;
    bottom: 0;
    background: linear-gradient(270deg, #00dd58 0%, #00ad45 100%);
    border-radius: 12px;
  }
  &.is-compleated {
    border: 1px solid rgba(23, 24, 24, 0.15);
    background: transparent;
    box-shadow: none;
  }
  &.is-locked {
    background: rgba(#fff, 0.6);
    box-shadow: none;
    pointer-events: none;
  }
}
</style>
