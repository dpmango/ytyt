<template>
  <div class="lessons">
    <div class="container">
      <LayoutBack :to="`/`" title="Вернуться к списку" />

      <div v-if="theme" class="lessons__title">
        <h1 class="h2-title">{{ theme.title }}</h1>
        <div class="lessons__title-stats">
          <span>{{ stats }}</span>
        </div>
      </div>

      <template v-else>
        <UiLoader :loading="true" theme="block" />
      </template>

      <div class="list">
        <div v-for="lesson in list" :key="lesson.id" class="list__row">
          <NuxtLink
            class="card"
            :class="[lesson.status === 3 && 'is-compleated', lesson.status === 4 && 'is-locked']"
            :to="`/theme/${$route.params.id}/${lesson.id}`"
          >
            <div class="card__num">{{ lesson.id }}</div>
            <div class="card__content">
              <div class="card__title">{{ lesson.title }}</div>
              <div class="card__description">{{ lesson.description }}</div>
            </div>
            <div class="card__status">
              <CoursePartStatus :status="lesson.status" />
            </div>
          </NuxtLink>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import Plurize from '~/helpers/Plurize';

export default {
  props: {
    themes: Array,
    list: Array,
  },
  computed: {
    theme() {
      const theme = this.themes.find((x) => x.id === parseInt(this.$route.params.id));
      if (theme) {
        return theme;
      }

      return null;
    },
    stats() {
      const plural = Plurize(this.theme.count_lessons, 'урок', 'урока', 'уроков');
      return `${this.theme.completed_count_lessons} / ${this.theme.count_lessons} ${plural}`;
    },
  },
};
</script>

<style lang="scss" scoped>
.lessons {
  padding-top: 24px;
  &__title {
    // h1 instance with h2 class
    margin: 4px 0 0;
  }
  &__title-stats {
    margin-top: 6px;
    font-size: 15px;
  }
}

.list {
  padding-top: 24px;
  &__row {
    margin-bottom: 8px;
  }
}

.card {
  position: relative;
  z-index: 1;
  display: flex;
  align-items: flex-start;
  background: #fff;
  box-shadow: 0 6px 24px -4px rgba(23, 24, 24, 0.1);
  border-radius: 8px;
  padding: 14px 48px 14px 20px;
  transition: box-shadow 0.25s $ease;
  &:hover {
    box-shadow: 0 8px 26px -2px rgba(23, 24, 24, 0.18);
  }
  &__num {
    flex: 0 0 10px;
    margin-top: 2px;
    font-size: 17px;
    color: #939598;
  }
  &__content {
    flex: 1 1 auto;
    padding-left: 20px;
    padding-right: 20px;
  }
  &__status {
    flex: 0 0 auto;
    display: inline-flex;
    align-items: center;
    margin-top: 6px;
    font-size: 14px;
    line-height: 1;
    .svg-icon {
      margin-right: 8px;
    }
  }
  &__title {
    font-weight: 500;
    font-size: 17px;
    line-height: 1.4;
  }
  &__description {
    margin-top: 6px;
    font-size: 14px;
  }
  &.is-compleated {
    border: 1px solid rgba(23, 24, 24, 0.15);
    opacity: 0.6;
    background: transparent;
    box-shadow: none;
  }
  &.is-locked {
    background: rgba(#fff, 0.6);
    box-shadow: none;
    pointer-events: none;
  }
}

@include r($sm) {
  .card {
    padding: 16px 16px;
    flex-direction: column;
    &__num {
      position: absolute;
      margin-top: 0;
      top: 14px;
      right: 16px;
    }
    &__status {
      order: 1;
      margin-top: 0;
    }
    &__content {
      order: 2;
      margin-top: 8px;
      padding-left: 0;
      padding-right: 0;
    }
  }
}
</style>
