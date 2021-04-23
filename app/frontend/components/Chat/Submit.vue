<template>
  <div class="chat-submit">
    <client-only>
      <template slot="placeholder">
        <UiLoader :loading="true" theme="block" />
      </template>

      <form class="chat-submit__form" @submit.prevent="handleSubmit">
        <UiMarkdownEditor @change="(v) => (text = v)" />

        <UiButton type="submit">Отправить</UiButton>
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
    };
  },
  computed: {
    ...mapGetters('chat', ['activeDialog']),
  },
  methods: {
    handleSubmit() {
      if (this.text.trim().length >= 1) {
        this.sendMessage({ body: this.text, dialog_id: this.activeDialog });

        this.text = '';

        this.$emit('messageSend');
      }
    },
    ...mapActions('chat', ['sendMessage', 'uploadFile']),
  },
};
</script>

<style lang="scss" scoped>
.chat-submit {
  &__form {
    display: flex;
    .vue-simplemde {
      flex: 1 1 auto;
    }
  }
}

// ::v-deep .CodeMirror,
// ::v-deep.CodeMirror-scroll {
//   min-height: 200px;
// }
</style>
