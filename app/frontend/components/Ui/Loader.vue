<template>
  <div class="loader" :class="[theme]">
    <BeatLoader :loading="loading" :color="color" :size="size" />
  </div>
</template>

<script>
import BeatLoader from 'vue-spinner/src/BeatLoader.vue';

export default {
  name: 'Loader',
  components: {
    BeatLoader,
  },
  props: {
    color: {
      type: String,
      default: '#1E88E5',
    },
    size: {
      type: String,
      default: '10px',
    },
    loading: {
      type: Boolean,
      default: false,
    },
    theme: {
      type: String,
      default: 'inline',
      validator: (theme) => ['inline', 'block'].includes(theme),
    },
  },
};
</script>

<style lang="scss" scoped>
.loader {
  &.block {
    display: flex;
    justify-content: center;
    margin: 16px 0;
  }
}

.v-spinner {
  display: flex;
  font-size: 0;
}
</style>
