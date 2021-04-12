<template>
  <div class="back" @click="goBack">
    <UiSvgIcon name="arrow-left-filled" />
    <span>{{ title }}</span>
  </div>
</template>

<script>
export default {
  props: {
    title: String,
  },
  methods: {
    goBack() {
      return this.$router.go(-1);
    },
  },
};
</script>

<style lang="scss" scoped>
.back {
  display: inline-flex;
  align-items: center;
  font-size: 14px;
  line-height: 1.5;
  color: $colorPrimary;
  cursor: pointer;
  transition: color 0.25s $ease;
  .svg-icon {
    font-size: 18px;
    margin-right: 8px;
  }
  &:hover {
    color: $fontColor;
  }
}
</style>
