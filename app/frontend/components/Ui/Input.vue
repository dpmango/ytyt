<template>
  <div class="input" :class="[{ 'has-error': error }, theme]">
    <label v-if="label" :for="_uid" class="input__label">{{ getLabel }}</label>
    <div class="input__input" :class="[{ 'is-iconed': icon || clearable, 'is-clearable': isClearable }, iconPosition]">
      <input
        v-if="!isTextArea"
        :id="_uid"
        :value="value"
        :placeholder="placeholder"
        v-bind="$attrs"
        v-on="$listeners"
        @input="setValue"
      />
      <textarea v-else :id="_uid" :value="value" :placeholder="placeholder" v-bind="$attrs" @input="setValue" />

      <span v-if="icon" class="input__icon" :class="[iconPosition]">
        <UiSvgIcon :name="icon" />
      </span>
      <span v-if="clearable" class="input__clear" @click="clearInput">
        <span>Отмена</span>
      </span>
    </div>
  </div>
</template>

<script>
export default {
  name: 'Input',
  props: {
    value: {
      type: String,
      required: false,
    },
    label: {
      type: String,
      required: false,
    },
    placeholder: {
      type: String,
      required: false,
    },
    icon: {
      type: String,
      required: false,
    },
    iconPosition: {
      type: String,
      required: false,
    },
    error: {
      type: [String, Boolean],
      required: false,
    },
    clearable: {
      type: Boolean,
      required: false,
    },
    theme: {
      type: String,
      required: false,
    },
  },
  computed: {
    isTextArea() {
      return this.$attrs.textarea !== undefined;
    },
    isClearable() {
      if (this.clearable) {
        return this.value && this.value.replace(/^\s+|\s+$/g, '').length > 1;
      } else {
        return false;
      }
    },
    getLabel() {
      return typeof this.error === 'string' ? this.parseVeeError(this.error) : this.label;
    },
  },
  methods: {
    setValue(e) {
      this.$emit('onChange', e.target.value);
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
.input {
  &__label {
    display: block;
    font-size: 12px;
    line-height: 16px;
    color: $fontColor;
    margin-bottom: 5px;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
  }

  &__input {
    position: relative;
    z-index: 1;
    input,
    textarea {
      -webkit-appearance: none;
      display: block;
      width: 100%;
      padding: 13px 14px;
      border: 1px solid transparent;
      background: $colorBg;
      border-radius: 5px;
      font-family: $baseFont;
      font-size: 14px;
      font-style: normal;
      font-weight: 400;
      line-height: 20px;
      color: $fontColor;
      transition: border 0.25s $ease, color 0.25s $ease, background 0.25s $ease;
      &::placeholder {
        color: $colorGray;
      }
      &:focus,
      &:active {
        border-color: $colorPrimary;
        outline: none;
      }
      &:hover {
        background-color: #f0f1f2;
      }
      &[readonly],
      &[disabled] {
        color: $colorGray;
        &:focus,
        &:active {
          border-color: transparent;
        }
      }
    }
    textarea {
      resize: vertical;
    }
    &.is-iconed {
      input,
      textarea {
        padding-right: 45px;
      }
      &.left {
        input,
        textarea {
          padding-left: 45px;
          padding-right: 14px;
        }
      }
    }
    &.is-clearable {
      input,
      textarea {
        padding-right: 45px;
      }
      .input__clear {
        opacity: 1;
        pointer-events: all;
      }
      &.is-iconed {
        .input__icon:not(.left) {
          opacity: 0;
          pointer-events: none;
        }
      }
    }
  }
  &__icon {
    position: absolute;
    z-index: 2;
    right: 15px;
    top: 50%;
    transform: translateY(-50%);
    font-size: 0;
    pointer-events: none;
    transition: opacity 0.25s $ease, fill 0.25s $ease;
    &.left {
      left: 15px;
      right: auto;
    }
    .svg-icon {
      font-size: 16px;
      color: $colorGray;
    }
  }
  &__clear {
    position: absolute;
    z-index: 2;
    right: 0;
    top: 50%;
    transform: translateY(-50%);
    padding: 8px 16px 7px 16px;
    color: $colorPrimary;
    font-size: 14px;
    line-height: 150%;
    cursor: pointer;
    opacity: 0;
    pointer-events: none;
    transition: color 0.25s $ease;
    &::before {
      display: inline-block;
      content: ' ';
      position: absolute;
      left: 0;
      top: 0;
      bottom: 0;
      width: 1px;
      background: rgba(#171818, 0.1);
    }
    &:hover {
      color: $fontColor;
    }
  }
  &.has-error {
    .input__input {
      input,
      textarea {
        border-color: $colorRed;
      }
    }
    .input__label {
      color: $colorRed;
    }
  }
}

input[type='search']::-webkit-search-decoration,
input[type='search']::-webkit-search-cancel-button,
input[type='search']::-webkit-search-results-button,
input[type='search']::-webkit-search-results-decoration {
  -webkit-appearance: none;
}
</style>
