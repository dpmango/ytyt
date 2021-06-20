<template>
  <div class="page">
    <LayoutHeader />
    <div class="page__content header-pad">
      <AuthNotificationConfirmation v-if="showConfirmationNotification" />
      <Nuxt />
    </div>
    <PaymentModals />
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
    // console.log('default mounted  -connect ?', !this.isConnected);

    if (!this.isConnected) {
      this.connect();
    } else {
      try {
        this.getDialogs();
        this.getNotificationCount();
      } catch (e) {
        this.$toast.global.error({ message: 'Ошибка подключения к сообщениям. Перезагрузите страницу' });
      }
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
