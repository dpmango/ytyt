<template>
  <div class="themes">
    <div class="container">
      <div class="back" @click="goBack">Вернуться к списку</div>
      <div class="list">
        <div v-for="theme in list" :key="theme.id" class="list__row">
          <NuxtLink
            class="card"
            :class="[theme.status === 3 && 'is-compleated', theme.status === 4 && 'is-locked']"
            :to="`/course/${$route.params.id}/${theme.id}`"
          >
            <div class="card__num">{{ theme.id }}</div>
            <div class="card__content">
              <div class="card__title">{{ theme.title }}</div>
              <div class="card__description">{{ theme.description }}</div>
            </div>
            <div class="card__status">
              <template v-if="theme.status === 1">
                <UiSvgIcon name="lock" />
                <span>Доступен</span>
              </template>
              <template v-if="theme.status === 2">
                <UiSvgIcon name="time" />
                <span>В процессе</span>
              </template>
              <template v-if="theme.status === 3">
                <UiSvgIcon name="checkmark" />
                <span>Завершен</span>
              </template>
              <template v-if="theme.status === 4">
                <UiSvgIcon name="lock" />
                <span>Заблокирован</span>
              </template>
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
  methods: {
    goBack() {
      return this.$router.go(-1);
    },
  },
};
</script>

<style lang="scss" scoped>
.themes {
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
    .card__status {
      color: $colorGreen;
    }
  }
  &.is-locked {
    background: rgba(#fff, 0.6);
    box-shadow: none;
    .card__status {
      color: rgba($fontColor, 0.7);
    }
  }
}
</style>
