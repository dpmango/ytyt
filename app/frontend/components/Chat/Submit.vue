<template>
  <div class="chat-submit">
    <template slot="placeholder">
      <UiLoader :loading="true" theme="block" />
    </template>

    <form class="chat-submit__form" @submit.prevent="handleSubmit">
      <div class="editor">
        <input :id="_uid" ref="uploadInput" type="file" @change="handleUpload" />

        <label :for="_uid" class="editor__attach" @click="handleAttachClick">
          <UiSvgIcon name="paper-clip" />
        </label>
        <div class="editor__body">
          <vue-simplemde
            ref="markdownEditor"
            v-model="text"
            :highlight="true"
            :configs="config"
            preview-class="markdown-body"
          />
        </div>
      </div>
    </form>
  </div>
</template>

<script>
import { mapActions, mapGetters } from 'vuex';
import { bytesToMegaBytes } from '~/helpers/FormatBytes';

export default {
  props: {},
  data() {
    return {
      text: '',
      uploader: {
        allowedMime: ['image'],
        maxSize: '5',
      },
      config: {
        autoDownloadFontAwesome: false,
        spellChecker: false,
        status: false,
        toolbar: false,
        placeholder: 'Сообщение...',
      },
    };
  },
  computed: {
    simplemde() {
      return this.$refs.markdownEditor.simplemde;
    },
    ...mapGetters('chat', ['activeDialog']),
  },
  mounted() {
    if (this.simplemde) {
      this.simplemde.codemirror.on('keydown', (instance, event) => {
        if ((event.ctrlKey || event.shiftKey) && event.keyCode === 13) {
          this.text += '\n';
        } else if (event.keyCode === 13) {
          event.preventDefault();
          this.handleSubmit();
        }
      });
    }
  },
  methods: {
    handleSubmit() {
      if (this.text.trim().length >= 1) {
        this.sendMessage({ body: this.text, dialog_id: this.activeDialog });

        this.text = '';
        this.simplemde.value('');
        this.$emit('onSubmit');
        // this.simplemde.codemirror.refresh();
      }
    },
    async handleUpload(e) {
      const files = e.target.files;

      if (files && files[0]) {
        const file = files[0];

        // limit size
        if (this.uploader.maxSize) {
          const sizeInMb = bytesToMegaBytes(file.size);

          if (sizeInMb > this.maxSize) {
            this.$toast.global.error({ message: `Размер изображения превышает ${this.maxSize}Мб` });
            return false;
          }
        }

        if (file) {
          const res = await this.uploadFile(file).catch((err) => {
            this.$toast.global.error({ message: err.data });
          });

          this.sendMessage({ file_id: res.id, dialog_id: this.activeDialog });
        }

        // if (this.includeReader) {
        //   const reader = new FileReader();
        //   reader.onload = (ev) => {
        //     this.setFileReaderValue(ev.target.result);
        //   };
        //   reader.readAsDataURL(file);
        // }
      }
    },
    handleAttachClick() {
      // this.simplemde.drawImage();
    },
    ...mapActions('chat', ['sendMessage', 'uploadFile']),
  },
};
</script>

<style lang="scss">
@import 'simplemde/dist/simplemde.min.css';

.CodeMirror,
.CodeMirror-scroll {
  min-height: 1px;
  max-height: 300px;
}

.CodeMirror {
  padding: 8px 16px 8px 0;
  border: 0;
}

.CodeMirror-scroll {
  margin-bottom: -50px;
  padding-bottom: 50px;
}
</style>

<style lang="scss" scoped>
.chat-submit {
  &__form {
    display: flex;
    align-items: center;
    padding-right: 10px;
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
}

.editor {
  display: flex;
  align-items: center;
  flex: 1 1 auto;
  padding-left: 10px;
  &__attach {
    flex: 0 0 auto;
    padding: 10px;
    font-size: 0;
    color: $colorGray;
    cursor: pointer;
    transition: color 0.25s $ease;
    .svg-icon {
      font-size: 20px;
    }
    &:hover {
      color: $fontColor;
    }
  }
  &__body {
    position: relative;
    flex: 1 1 auto;
  }
}

// .vue-simplemde {
//   .markdown-body {
//     padding: 8px 16px 8px 8px !important;
//   }
// }
</style>
