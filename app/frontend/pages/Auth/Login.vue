<template>
  <AuthLogin />
</template>

<script>
export default {
  layout: 'auth',
  head: {
    title: 'Авторизация',
  },
  mounted() {
    if (this.$store.getters['auth/isAuthenticated']) {
      this.$router.push('/course');
    }
  },
};
</script>
