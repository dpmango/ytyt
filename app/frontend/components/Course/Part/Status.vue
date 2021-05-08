<template>
  <div
    class="status"
    :class="[
      status === 1 && 'is-available',
      status === 2 && 'is-current',
      status === 3 && 'is-compleated',
      [4, 5, 6, 7, 8].includes(status) && 'is-locked',
    ]"
  >
    {{ constants }}
    <template v-if="status === 1">
      <UiSvgIcon name="radio" />
    </template>
    <template v-if="status === 2">
      <UiSvgIcon name="time" />
    </template>
    <template v-if="status === 3">
      <UiSvgIcon name="checkmark" />
    </template>
    <template v-if="[4, 5, 6, 7, 8].includes(status)">
      <UiSvgIcon name="lock" />
    </template>
    <span>{{ constant }}</span>
  </div>
</template>

<script>
import { mapGetters } from 'vuex';

export default {
  props: {
    status: Number,
  },
  computed: {
    constant() {
      return this.getConstantById(this.status);
    },
    ...mapGetters('constants', ['getConstantById', 'constants']),
  },
};
</script>

<style lang="scss" scoped>
.status {
  flex: 0 0 auto;
  display: inline-flex;
  align-items: center;
  font-size: 14px;
  line-height: 1;
  .svg-icon {
    margin-right: 8px;
  }
  &.is-available {
    color: rgba($fontColor, 0.7);
  }
  &.is-current {
    color: rgba($fontColor, 0.7);
  }
  &.is-compleated {
    color: $colorGreen;
  }
  &.is-locked {
    color: rgba($fontColor, 0.7);
  }
}
</style>
