/* eslint-disable vue/no-v-html */
<template>
  <div class="lessons">
    <div class="container">
      <div class="back" @click="goBack">Вернуться к списку тем</div>
      <div class="list">
        <div v-for="lesson in list" :key="lesson.id" class="list__row">
          <div class="card">
            <div class="card__title">{{ lesson.title }}</div>

            <NuxtLink :to="`/course/${$route.params.course}/${lesson.course_theme}/${lesson.id}`">
              <UiButton>Начать курс</UiButton>
            </NuxtLink>

            <div class="card__body" v-html="lesson.description"></div>
          </div>
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
  methods: {
    goBack() {
      return this.$router.go(-1);
    },
  },
};
</script>

<style lang="scss" scoped>
.lessons {
  padding-top: 24px;
}

.back {
  font-size: 14px;
  line-height: 1.5;
  color: $colorPrimary;
  cursor: pointer;
  transition: color 0.25s $ease;
  &:hover {
    color: $fontColor;
  }
}

.list {
  padding-top: 24px;
  &__row {
    margin-bottom: 24px;
  }
}

.card {
  background: #fff;
  box-shadow: 0 6px 24px -4px rgba(23, 24, 24, 0.1);
  border-radius: 8px;
  padding: 14px 20px;
  transition: box-shadow 0.25s $ease;
  &:hover {
    box-shadow: 0 8px 26px -2px rgba(23, 24, 24, 0.18);
  }

  &__title {
    font-weight: 500;
    font-size: 17px;
    line-height: 1.5;
  }
  &__body {
    margin-top: 16px;
    padding-top: 1px;
    border-top: 1px solid $borderColor;
    font-size: 14px;
    line-height: 1.5;
  }
}
</style>
