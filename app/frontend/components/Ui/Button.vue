<template>
  <component
    :is="getElement"
    :class="['button', theme, size, isBlock, noPadding, { 'is-loading': showLoader }]"
    :href="href"
    :to="to"
    v-bind="$attrs"
    v-on="$listeners"
  >
    <slot />
    <UiLoader v-if="showLoader" :loading="showLoader" :color="loaderColor" />
  </component>
</template>

<script>
const loaderDelay = 300;

export default {
  name: 'Button',
  props: {
    href: {
      type: String,
      default: null,
    },
    to: {
      type: String,
      default: null,
    },
    theme: {
      type: String,
      default: 'primary',
      validator: (theme) => ['primary', 'outline', 'danger', 'success'].includes(theme),
    },
    size: {
      type: String,
      default: 'regular',
      validator: (theme) => ['regular', 'small'].includes(theme),
    },
    isLoading: {
      type: Boolean,
      required: false,
    },
    loaderColor: {
      type: String,
      required: false,
    },
  },
  data() {
    return {
      showLoader: false,
      timer: null,
    };
  },
  computed: {
    isBlock() {
      if (this.$attrs.block !== undefined) {
        return 'block';
      }
      return '';
    },
    noPadding() {
      if (this.$attrs['no-padding'] !== undefined) {
        return 'no-padding';
      }
      return '';
    },
    getElement() {
      if (this.href) {
        return 'a';
      } else if (this.to) {
        return 'NuxtLink';
      }

      return 'button';
    },
  },
  watch: {
    isLoading(newV, _oldV) {
      if (newV) {
        this.timer = setTimeout(() => {
          this.showLoader = true;
        }, loaderDelay);
      } else {
        clearTimeout(this.timer);
        this.showLoader = false;
      }
    },
  },
};
</script>

<style lang="scss" scoped>
.button {
  position: relative;
  display: inline-flex;
  justify-content: center;
  align-items: center;
  padding: 12px 23px;
  border: 2px solid transparent;
  box-sizing: border-box;
  border-radius: 8px;
  font-weight: 500;
  font-size: 17px;
  text-align: center;
  cursor: pointer;
  box-shadow: none;
  transition: background 0.25s $ease, color 0.25s $ease;
  &:focus,
  &:active {
    outline: none;
  }

  ::v-deep span {
    display: inline-block;
    margin-right: 7px;
  }
  ::v-deep svg {
    width: 15px;
    vertical-align: middle;
    transition: stroke 0.25s $ease;
  }

  &.primary {
    background: $colorPrimary;
    color: #fff;
    border-color: transparent;
    box-shadow: 0 6px 24px -4px rgba(23, 24, 24, 0.1);

    &:hover {
      background-color: $colorAccent;
    }
    &:active {
      background: $colorAccent;
    }
  }
  &.outline {
    color: $fontColor;
    background: transparent;
    border-color: $colorPrimary;
    &:hover {
      background: rgba($colorPrimary, 0.8);
      border-color: $colorPrimary;
    }
    &:active {
      background: transparent;
      border-color: $colorPrimary;
    }
  }
  &.danger {
    color: white;
    background: $colorRed;
    border-color: transparent;
    &:hover {
      background: rgba($colorRed, 0.8);
    }
    &:active {
      background: rgba($colorRed, 0.9);
    }
  }
  &.no-padding {
    padding: 0;
  }

  &.success {
    color: white;
    background: $colorGreen;
    border-color: transparent;
    &:hover {
      background: rgba($colorGreen, 0.8);
    }
    &:active {
      background: rgba($colorGreen, 0.9);
    }
  }

  &.small {
    font-size: 15px;
    padding: 7px 14px;
  }
  &.block {
    display: block;
    width: 100%;
  }

  &[disabled] {
    background: rgba($fontColor, 0.3);
    color: rgba($fontColor, 0.7);
    pointer-events: none;
  }

  .loader {
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
  }
  &.is-loading {
    color: transparent !important;
  }
}
</style>
