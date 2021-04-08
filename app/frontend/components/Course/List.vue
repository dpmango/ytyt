<template>
  <div class="list">
    <div class="container">
      <div class="row">
        <div v-for="course in list" :key="course.id" class="col col-3 col-lg-4 col-md-6 col-sm-12">
          <NuxtLink class="card" :to="`/course/${course.id}`">
            <div class="card__status">TBD (status)</div>
            <div class="card__title">{{ course.title }}</div>
            <div class="card__description">TBD - no need ? {{ course.description }}</div>
            <div class="card__cost">TBD {{ course.cost }} рублей</div>
            <div class="card__stats">
              <span>{{ course.count_themes }} темы</span>
              <span>{{ course.count_lessons }} урока</span>
            </div>
            <div class="card__progress">
              <div class="card__progress-inner" :style="{ width: '30%' }"></div>
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
.list {
  padding-top: 24px;
}

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
  &__status {
    font-size: 14px;
    line-height: 150%;
    opacity: 0.7;
  }
  &__title {
    margin-top: 8px;
    font-weight: 500;
    font-size: 17px;
    line-height: 1.35;
  }
  &__description {
    font-size: 14px;
    line-height: 1.5;
    opacity: 0.7;
  }
  &__cost {
    font-size: 14px;
    line-height: 1.5;
  }
  &__stats {
    margin-top: auto;
    padding-top: 34px;
    display: flex;
    align-items: center;
    font-size: 14px;
    line-height: 1.5;
    span {
      margin-right: 16px;
      &:last-child {
        margin-right: 0;
      }
    }
  }
  &__progress {
    position: relative;
    margin-top: 6px;
    background: rgba(23, 24, 24, 0.08);
    border-radius: 12px;
    height: 6px;
    font-size: 0;
  }
  &__progress-inner {
    position: absolute;
    top: 0;
    left: 0;
    bottom: 0;
    background: linear-gradient(270deg, #00dd58 0%, #00ad45 100%);
    border-radius: 12px;
  }
}
</style>
