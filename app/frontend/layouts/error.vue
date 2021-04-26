<template>
  <div class="container error">
    <h1 v-if="error.statusCode === 404">404 Page not found</h1>
    <h1 v-else>An error occurred</h1>
    <NuxtLink to="/">Вернуться на главную</NuxtLink>
  </div>
</template>

<script>
export default {
  props: {
    error: Object,
  },
  mouted() {
    console.log(this.error);
  },
};
</script>

<style lang="scss">
.error {
  margin-top: 2em;
}
</style>
