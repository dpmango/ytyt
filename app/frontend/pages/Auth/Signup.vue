<template>
  <AuthSignup />
</template>

<script>
export default {
  layout: 'auth',
  middleware: ['authenticated'],
  head: {
    title: 'Регистрация | YtYt - понятные уроки программирования',
  },
};
</script>
