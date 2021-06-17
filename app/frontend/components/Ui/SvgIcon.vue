<template>
  <svg
    v-if="icon"
    :style="{ width: width }"
    :viewBox="viewBox"
    :class="className"
    preserveAspectRatio="none"
    v-html="icon"
  />
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
      viewBox: '0 0 0 0',
      width: '1em',
      icon: undefined,
    };
  },
  computed: {
    className() {
      return 'svg-icon svg-icon--' + this.name;
    },
  },
  mounted() {
    try {
      const iconRaw = require(`~/assets/icons/${this.name}.svg?raw`);

      // parse from DOM
      const parser = new DOMParser();
      const svg = parser.parseFromString(iconRaw, 'image/svg+xml');
      const viewBox = svg.querySelector('svg').getAttribute('viewBox');
      const body = svg.querySelector('svg').innerHTML.replace(/fill="([^"]+)"/g, '');

      // calculate
      // const body = iconRaw.replace(/<svg[^>]+>/g, '').replace('</svg>', '');
      const size = viewBox.split(' ').slice(2);

      if (size.length === 2) {
        const ratio = `${(size[0] / size[1]).toFixed(2)}em`;

        // SET
        this.width = ratio;
        this.viewBox = viewBox;
        this.icon = body;
      }
    } catch (err) {
      // eslint-disable-next-line no-console
      console.warn('error loading svg icon', err);
    }
  },
};
</script>
