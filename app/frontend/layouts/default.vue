<template>
  <div class="page">
    <LayoutHeader />
    <div class="page__content header-pad">
      <Nuxt />
    </div>
  </div>
</template>

<script>
export default {
  middleware: ['auth'],
};
</script>

<style lang="scss">
.header-pad {
  padding-top: 56px;
}
</style>
