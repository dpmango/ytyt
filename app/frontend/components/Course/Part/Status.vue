<template>
  <div
    class="status"
    :class="[
      status === 1 && 'is-available',
      status === 2 && 'is-current',
      status === 3 && 'is-compleated',
      status === 4 && 'is-locked',
    ]"
  >
    <template v-if="status === 1">
      <UiSvgIcon name="radio" />
      <span>Доступен</span>
    </template>
    <template v-if="status === 2">
      <UiSvgIcon name="time" />
      <span>В процессе</span>
    </template>
    <template v-if="status === 3">
      <UiSvgIcon name="checkmark" />
      <span>Завершен</span>
    </template>
    <template v-if="status === 4">
      <UiSvgIcon name="lock" />
      <span>Заблокирован</span>
    </template>
  </div>
</template>

<script>
export default {
  props: {
    status: Number,
  },
};
</script>

<style lang="scss" scoped>
.status {
  flex: 0 0 auto;
  display: inline-flex;
  align-items: center;
  font-size: 14px;
  line-height: 1;
  .svg-icon {
    margin-right: 8px;
  }
  &.is-available {
    color: rgba($fontColor, 0.7);
  }
  &.is-current {
    color: rgba($fontColor, 0.7);
  }
  &.is-compleated {
    color: $colorGreen;
  }
  &.is-locked {
    color: rgba($fontColor, 0.7);
  }
}
</style>
