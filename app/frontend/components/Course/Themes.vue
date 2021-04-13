<template>
  <div class="list">
    <div class="container">
      <div class="row">
        <div v-for="theme in list" :key="theme.id" class="col col-3 col-lg-4 col-md-6 col-sm-12">
          <CoursePartTheme :theme="theme" />
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
</style>
