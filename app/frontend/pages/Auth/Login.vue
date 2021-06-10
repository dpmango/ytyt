<template>
  <AuthLogin />
</template>

<script>
export default {
  layout: 'auth',
  middleware: ['authenticated'],
  head: {
    title: 'Войти | YtYt - понятные уроки программирования',
  },
};
</script>
