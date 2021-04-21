<template>
  <div v-if="error" class="error">{{ error }}</div>
</template>

<script>
export default {
  name: 'Error',
  props: {
    error: {
      type: String,
    },
  },
};
</script>

<style lang="scss" scoped>
.error {
  background: rgba($colorRed, 0.1);
  border: 1px solid $colorRed;
  border-radius: 8px;
  padding: 8px 16px;
  font-size: 14px;
  font-weight: 500;
  color: $colorRed;
  text-align: center;
}
</style>
