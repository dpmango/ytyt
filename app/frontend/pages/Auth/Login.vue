<template>
  <AuthLogin />
</template>

<script>
export default {
  layout: 'auth',
  middleware: ['authenticated'],
  head: {
    title: 'Авторизация',
  },
};
</script>
