<template>
  <div class="toggle" :class="[{ 'has-error': error }, theme]">
    <label v-if="label" :for="_uid" class="toggle__label">{{ label }}</label>
    <div class="toggle__input">
      <input
        :id="_uid"
        type="checkbox"
        :checked="value"
        :value="value"
        v-bind="$attrs"
        v-on="$listeners"
        @input="setValue"
      />
      <div class="toggle__input-box"></div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'Input',
  props: {
    value: {
      type: Boolean,
      required: false,
    },
    label: {
      type: String,
      required: false,
    },
    error: {
      type: [String, Boolean],
      required: false,
    },
    theme: {
      type: String,
      required: false,
    },
  },
  computed: {},
  methods: {
    setValue(e) {
      this.$emit('onChange', !this.value);
    },
    clearInput() {
      if (this.isClearable) {
        this.$emit('onChange', '');
      }
    },
    parseVeeError(err) {
      return err.replaceAll('{field}', '');
    },
  },
};
</script>

<style lang="scss" scoped>
.toggle {
  position: relative;
  display: flex;
  align-items: center;
  &__label {
    position: relative;
    z-index: 2;
    font-size: 15px;
    padding-right: 76px;
    cursor: pointer;
    transition: opacity 0.25s $ease;
    &:hover {
      opacity: 0.8;
    }
  }
  &__input {
    position: relative;
    input {
      position: absolute;
      top: 0;
      left: 0;
      opacity: 0;
      width: 0.1px;
      height: 0.1px;
      overflow: hidden;
      &:checked + .toggle__input-box {
        background: #1e88e5;
        &::after {
          left: 29px;
        }
      }
    }
  }
  &__input-box {
    position: absolute;
    z-index: 1;
    right: 0;
    top: 50%;
    transform: translateY(-50%);
    width: 60px;
    height: 36px;
    background: $colorGray;
    border-radius: 100px;
    &::after {
      display: inline-block;
      content: ' ';
      position: absolute;
      top: 5px;
      left: 5px;
      width: 26px;
      height: 26px;
      background: #fff;
      box-shadow: 0 4px 4px rgba(0, 0, 0, 0.16);
      border-radius: 100px;
      transition: left 0.25s $ease;
    }
  }
}
</style>
