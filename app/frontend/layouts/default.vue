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
      if (['Messages'].includes(this.$route.name)) {
        return false;
      }

      return true;
    },
  },
  mounted() {
    if (!this.$store.getters['chat/isConnected']) {
      this.$store.dispatch('chat/connect');
    }
  },
};
</script>

<style lang="scss">
.header-pad {
  padding-top: 56px;
}
</style>
