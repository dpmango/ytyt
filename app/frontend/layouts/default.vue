<template>
  <div class="page">
    <div class="page__content">
      <Nuxt />
    </div>
  </div>
</template>

<script>
export default {
  middleware: ['auth'],
};
</script>
