<template>
  <vue-final-modal
    v-bind="$attrs"
    classes="modal-container"
    :content-class="['modal-content', contentClass]"
    v-on="$listeners"
  >
    <div class="modal__content">
      <slot></slot>
    </div>

    <!-- <button class="modal__close" @click="$emit('input', false)">
      <UiSvgIcon name="close" />
    </button> -->
  </vue-final-modal>
</template>

<script>
export default {
  name: 'Modal',
  inheritAttrs: false,
  props: {
    contentClass: String,
  },
};
</script>

<style lang="scss" scoped>
::v-deep .modal-container {
  display: flex;
  justify-content: center;
  align-items: center;
  padding-left: 16px;
  padding-right: 16px;
}
::v-deep .modal-content {
  position: relative;
  display: flex;
  flex-direction: column;
  width: 100%;
  max-height: calc(100% - 40px);
  max-width: 880px;
  margin: 0 auto;
  padding: 0;
  background: #fff;
  box-shadow: 0 8px 26px -2px rgba(23, 24, 24, 0.18);
  border-radius: 8px;
  &.narrow {
    max-width: 420px;
    padding: 32px 30px;
    @include r($sm) {
      max-width: 328px;
      padding: 24px;
      .modal__close {
        top: 6px;
        right: 6px;
      }
    }
  }
}

.modal__content {
  position: relative;
  z-index: 1;
  flex-grow: 1;
  overflow: hidden;
  border-radius: 8px;
}
.modal__close {
  position: absolute;
  z-index: 3;
  top: 12px;
  right: 12px;
  width: 32px;
  height: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: rgba($fontColor, 0.5);
  cursor: pointer;
  outline: none;
  transition: color 0.25s $ease;
  .svg-icon {
    font-size: 18px;
  }
  &:hover {
    color: $colorRed;
  }
}
</style>
