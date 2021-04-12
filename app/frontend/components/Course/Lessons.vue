<template>
  <div class="lessons">
    <div class="container">
      <LayoutBack title="Вернуться к списку" />

      <div class="list">
        <div v-for="lesson in list" :key="lesson.id" class="list__row">
          <NuxtLink
            class="card"
            :class="[lesson.status === 3 && 'is-compleated', lesson.status === 4 && 'is-locked']"
            :to="`/course/${$route.params.course}/${$route.params.id}/${lesson.id}`"
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
export default {
  props: {
    list: Array,
  },
};
</script>

<style lang="scss" scoped>
.lessons {
  padding-top: 24px;
}

.list {
  padding-top: 24px;
  &__row {
    margin-bottom: 8px;
  }
}

.card {
  display: flex;
  align-items: flex-start;
  background: #fff;
  box-shadow: 0 6px 24px -4px rgba(23, 24, 24, 0.1);
  border-radius: 8px;
  padding: 14px 20px;
  transition: box-shadow 0.25s $ease;
  &:hover {
    box-shadow: 0 8px 26px -2px rgba(23, 24, 24, 0.18);
  }
  &__num {
    flex: 0 0 10px;
    margin-top: 2px;
    font-size: 17px;
    line-height: 1.5;
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
    line-height: 1.5;
  }
  &__description {
    margin-top: 6px;
    font-size: 14px;
    line-height: 1.5;
  }
  &.is-compleated {
    border: 1px solid rgba(23, 24, 24, 0.15);
    background: transparent;
    box-shadow: none;
  }
  &.is-locked {
    background: rgba(#fff, 0.6);
    box-shadow: none;
  }
}
</style>
