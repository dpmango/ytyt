<template>
  <div class="uploader" :class="[{ 'has-error': error }, theme]">
    <label v-if="label" :for="_uid" class="uploader__label"> {{ getLabel }}</label>

    <div class="uploader__wrapper">
      <input :id="_uid" ref="uploadInput" type="file" v-bind="$attrs" @change="handleUpload" />

      <slot :file="file" name="info">
        <div v-if="file" class="uploader__file">
          <div class="uploader__file-icon">
            <UiSvgIcon key="paper-clip" name="paper-clip" />
            <span class="uploader__file-name">{{ file.name }}</span>
          </div>
        </div>
      </slot>

      <slot :error="uploadError" name="error">
        <div v-if="uploadError" class="uploader__error">
          <div class="uploader__error-icon">
            <UiSvgIcon key="paper-clip" name="paper-clip" />
            <span class="uploader__error-name">{{ uploadError }}</span>
          </div>
        </div>
      </slot>

      <slot :trigger="triggerUploadWindow" name="button">
        <UiButton type="button" pad="light" @click="triggerUploadWindow">
          <template v-if="buttonText">{{ buttonText }}</template>
          <template v-else-if="uploadError || file"> Загрузите еще </template>
          <template v-else> Загрузить</template>
        </UiButton>
      </slot>
    </div>
  </div>
</template>

<script>
import { bytesToMegaBytes } from '~/helpers/FormatBytes';

export default {
  name: 'Uploader',
  components: {},
  props: {
    file: {
      type: Object,
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
    allowedMime: {
      type: Array,
      required: false,
    },
    maxSize: {
      type: Number,
      required: false,
    },
    includeReader: {
      type: Boolean,
      required: false,
    },
    buttonText: {
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
  data() {
    return {
      uploadError: undefined,
    };
  },
  computed: {
    getLabel() {
      return typeof this.error === 'string' ? this.parseVeeError(this.error) : this.label;
    },
  },
  watch: {
    uploadError(error) {
      // eslint-disable-next-line no-console
      console.log('erorr', error);
      this.$emit('handleError', error);
    },
  },
  methods: {
    setValue(file) {
      // console.log('uploader file - ', file)
      this.$emit('onChange', file);
    },
    setFileReaderValue(res) {
      this.$emit('onReader', res);
    },
    parseVeeError(err) {
      return err.replaceAll('{field}', '');
    },
    triggerUploadWindow() {
      this.$refs.uploadInput.click();
    },
    handleUpload(e) {
      const files = e.target.files;
      // cleanup
      this.uploadError = undefined;
      this.setValue(undefined);

      if (files && files[0]) {
        const file = files[0];

        // limit mime
        if (this.allowedMime) {
          const mimeType = file.type ? file.type.split('/')[0] : undefined;

          if (!this.allowedMime.includes(mimeType)) {
            this.uploadError = 'Неверный формат файла';
            return false;
          }
        }

        // limit size
        if (this.maxSize) {
          const sizeInMb = bytesToMegaBytes(file.size);

          if (sizeInMb > this.maxSize) {
            this.uploadError = `Размер изображения превышает ${this.maxSize}Мб`;
            return false;
          }
        }

        this.setValue(file);

        if (this.includeReader) {
          const reader = new FileReader();
          reader.onload = (ev) => {
            this.setFileReaderValue(ev.target.result);
          };
          reader.readAsDataURL(file);
        }
      }
    },
  },
};
</script>

<style lang="scss" scoped>
.uploader {
  &__label {
    display: block;
    font-size: 12px;
    line-height: 16px;
    color: $colorGray;
    margin-bottom: 10px;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
  }
  &__wrapper {
    position: relative;
    z-index: 1;
    display: flex;
    flex-wrap: wrap;
    align-items: center;
    input {
      position: absolute;
      left: 0;
      top: 0;
      width: 0.1px;
      height: 0.1px;
      opacity: 0;
      visibility: hidden;
    }
  }
  &__file,
  &__error {
    display: flex;
    align-items: center;
    margin-right: 35px;
    min-height: 36px;
  }
  &__file-icon {
    font-size: 0;
    svg {
      width: 14px;
      fill: $colorGray;
    }
  }
  &__file-name,
  &__error-name {
    display: inline-block;
    margin-left: 8px;
    font-size: 14px;
    font-weight: 400;
    line-height: 19px;
  }
  &__error-icon {
    font-size: 0;
    svg {
      width: 16px;
      fill: none;
      stroke: #ff3232;
    }
  }
  &__error-name {
    color: #ff3232;
  }
  &.has-error {
    .uploader__label {
      color: $colorRed;
    }
  }
  &.dark {
    .uploader__label {
      color: white;
    }
  }
}
</style>
