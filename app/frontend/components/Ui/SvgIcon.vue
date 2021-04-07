<template>
  <svg v-if="icon" :viewBox="icon.viewBox" :class="`z-icon z-icon-${name}`" preserveAspectRatio="none">
    <use :xlink:href="icon.url"></use>
  </svg>
</template>

<script>
export default {
  name: 'SvgIcon',
  props: {
    name: {
      type: String,
      required: true,
    },
  },
  data() {
    return {
      icon: '',
    };
  },
  mounted() {
    this.icon = require(`~/assets/icons/${this.name}.svg`).default;
  },
};
</script>
