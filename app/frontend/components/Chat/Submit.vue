<template>
  <div class="chat-submit">
    <template slot="placeholder">
      <UiLoader :loading="true" theme="block" />
    </template>

    <form class="chat-submit__form" @submit.prevent="handleSubmit">
      <div class="editor">
        <input :id="_uid" ref="uploadInput" type="file" @change="handleUpload" />

        <label :for="_uid" class="editor__attach">
          <UiSvgIcon name="paper-clip" />
        </label>
        <div class="editor__body">
          <div v-if="reply.id" class="editor__reply">
            <span class="editor__reply-title">Ответ на: {{ reply.text }}</span>
            <div class="editor__reply-delete" @click="handleReplyDelete">
              <UiSvgIcon name="close" />
            </div>
          </div>
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
import { mapActions, mapMutations, mapGetters } from 'vuex';
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
    ...mapGetters('chat', ['activeDialog', 'reply']),
  },
  mounted() {
    if (this.simplemde) {
      this.simplemde.codemirror.on('keydown', (instance, event) => {
        if ((event.ctrlKey || event.shiftKey) && event.keyCode === 13) {
          event.preventDefault();
          const cursor = this.simplemde.codemirror.getCursor();

          this.simplemde.codemirror.replaceRange('\r\n', {
            line: cursor.line,
            ch: cursor.ch,
          });

          this.simplemde.codemirror.scrollIntoView({ line: cursor.line + 1, char: cursor.ch }, 200);
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
        const request = { body: this.text, dialog_id: this.activeDialog };

        // getting lesson id from url
        const loc = window.location.href.split('/');
        if (loc.includes('theme')) {
          request.lesson_id = parseInt(loc[loc.length - 1]);
        }

        if (this.reply.id) {
          request.reply_id = this.reply.id;
        }

        this.sendMessage(request);

        this.text = '';
        this.simplemde.value('');
        this.$emit('onSubmit');
        // this.simplemde.codemirror.refresh();
      }
    },
    async handleUpload(e) {
      // cleanup

      const files = e.target.files;

      if (files && files[0]) {
        const file = files[0];

        // limit size
        if (this.uploader.maxSize) {
          const sizeInMb = bytesToMegaBytes(file.size);

          if (sizeInMb > this.maxSize) {
            await this.$toast.global.error({ message: `Размер файла превышает ${this.maxSize}Мб` });
            e.target.value = '';
            return false;
          }
        }

        if (file) {
          await this.createMessageGhost({ file });

          this.$emit('onSubmit');

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

        e.target.value = '';
      }
    },
    handleReplyDelete() {
      this.setReply({
        id: null,
        text: null,
      });
    },
    ...mapActions('chat', ['sendMessage', 'uploadFile', 'createMessageGhost']),
    ...mapMutations('chat', ['setReply']),
  },
};
</script>

<style lang="scss">
@import 'simplemde/dist/simplemde.min.css';

.chat-submit {
  .CodeMirror,
  .CodeMirror-scroll {
    min-height: 1px;
    height: 100%;
    max-height: 340px;
  }

  .CodeMirror {
    // padding: 8px 16px 8px 0;
    padding: 0 16px 0 0;
    border: 0;
    font-size: 15px;
    line-height: 1.5;
  }

  .CodeMirror-scroll {
    margin-bottom: -50px;
    padding-bottom: 50px;
  }
}
</style>

<style lang="scss" scoped>
.chat-submit {
  &__form {
    display: flex;
    align-items: center;
    padding-right: 10px;
    padding-top: 8px;
    padding-bottom: 8px;
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
  &__reply {
    display: inline-flex;
    align-items: center;
    padding-top: 6px;
    padding-left: 5px;
    font-size: 14px;
  }
  &__reply-title {
    opacity: 0.6;
    text-decoration: underline;
    text-decoration-style: dashed;
  }
  &__reply-delete {
    cursor: pointer;
    margin-left: 4px;
    padding: 4px;
    font-size: 0;
    opacity: 0.6;
    transition: opacity 0.25s $ease, color 0.25s $ease;
    .svg-icon {
      font-size: 12px;
    }
    &:hover {
      opacity: 1;
      color: $colorRed;
    }
  }
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
