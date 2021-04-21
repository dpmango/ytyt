<template>
  <div class="page">
    <LayoutHeader />
    <div class="page__content header-pad">
      <AuthNotificationConfirmation v-if="showConfirmationNotification" />
      <Nuxt />
    </div>
  </div>
</template>

<script>
export default {
  middleware: ['auth'],
  computed: {
    showConfirmationNotification() {
      if (this.$route.name === 'Messages') {
        return false;
      }

      return true;
    },
  },
};
</script>

<style lang="scss">
.header-pad {
  padding-top: 56px;
}
</style>
