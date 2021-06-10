<template>
  <LandingHome />
</template>

<script>
export default {
  layout: 'clear',
  middleware: ['authenticated'],
  head: {
    title: 'Понятные уроки программирования | YtYt',
  },
};
</script>
