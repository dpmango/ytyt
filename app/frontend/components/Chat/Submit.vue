<template>
  <div class="chat-submit">
    <client-only>
      <template slot="placeholder">
        <UiLoader :loading="true" theme="block" />
      </template>

      <form class="chat-submit__form" @submit.prevent="handleSubmit">
        <div class="editor">
          <div class="editor__attach" @click="handleAttachClick">
            <UiSvgIcon name="paper-clip" />
          </div>
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

        <div class="chat-submit__submit">
          <UiButton type="submit">Отправить</UiButton>
        </div>
      </form>
    </client-only>
  </div>
</template>

<script>
import { mapActions, mapGetters } from 'vuex';

export default {
  props: {
    messageSend: Function,
  },
  data() {
    return {
      text: '',
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
  methods: {
    handleSubmit() {
      if (this.text.trim().length >= 1) {
        this.sendMessage({ body: this.text, dialog_id: this.activeDialog });

        this.text = '';
        this.simplemde.value('');
        this.$emit('messageSend');
        // this.simplemde.codemirror.refresh();
      }
    },
    handleAttachClick() {
      this.simplemde.drawImage();
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
  padding: 8px 16px 8px 16px;
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
  }
  &__submit {
    .button {
      padding: 7px 12px;
      font-size: 14px;
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
