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
import { mapGetters, mapActions } from 'vuex';

export default {
  middleware: ['default'],

  computed: {
    showConfirmationNotification() {
      if (!this.$route.name || ['Messages'].includes(this.$route.name)) {
        return false;
      }

      return true;
    },
    ...mapGetters('chat', ['isConnected']),
  },
  watch: {
    isConnected(newVal, oldVal) {
      if (newVal === true) {
        this.getDialogs();
        this.getNotificationCount();
      }
    },
  },
  mounted() {
    if (!this.isConnected) {
      this.connect();
    }
  },
  methods: {
    ...mapActions('chat', ['connect', 'getDialogs', 'getNotificationCount']),
  },
};
</script>

<style lang="scss">
.header-pad {
  padding-top: 56px;
}
</style>
