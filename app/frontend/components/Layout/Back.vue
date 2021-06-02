<template>
  <div class="back" :data-to="to" @click="goBack">
    <UiSvgIcon name="arrow-left-filled" />
    <span>{{ title }}</span>
  </div>
</template>

<script>
export default {
  props: {
    title: String,
    to: String,
  },
  methods: {
    goBack() {
      return this.$router.push(this.to);
      // return this.$router.go(-1);
    },
  },
};
</script>

<style lang="scss" scoped>
.back {
  display: inline-flex;
  align-items: center;
  font-size: 14px;
  color: $colorPrimary;
  cursor: pointer;
  transition: color 0.25s $ease;
  span {
    vertical-align: middle;
  }
  .svg-icon {
    font-size: 20px;
    margin-right: 8px;
  }
  &:hover {
    color: $colorPrimaryHover;
  }
}
</style>
