<template>
  <AuthSignup />
</template>

<script>
export default {
  layout: 'auth',
  head: {
    title: 'Регистрация',
  },
  mounted() {
    if (this.$store.getters['auth/isAuthenticated']) {
      this.$router.push('/course');
    }
  },
};
</script>
