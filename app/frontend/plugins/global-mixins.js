import Vue from 'vue';

const mixins = {
  methods: {
    modal(flag) {
      this.$bus.$emit('on-modal', flag);
    },
  },
};

Vue.mixin(mixins);
