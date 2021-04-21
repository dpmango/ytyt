<template>
  <div class="chat-submit">
    <client-only>
      <template slot="placeholder">
        <UiLoader :loading="true" theme="block" />
      </template>

      <ValidationObserver
        ref="form"
        v-slot="{ invalid }"
        tag="form"
        class="chat-submit__form"
        @submit.prevent="handleSubmit"
      >
        <ValidationProvider v-slot="{ errors }" rules="required">
          <UiMarkdownEditor @change="(v) => (text = v)" />
        </ValidationProvider>
        <UiButton type="submit">Отправить</UiButton>
      </ValidationObserver>
    </client-only>
  </div>
</template>

<script>
import { mapActions, mapGetters } from 'vuex';

export default {
  props: {},
  data() {
    return {
      text: '',
    };
  },
  computed: {},
  methods: {
    async handleSubmit() {
      const isValid = await this.$refs.form.validate();
    },
    // ...mapActions('auth', ['logout', 'getUserInfo', 'update']),
    // ...mapGetters('auth', ['user']),
  },
};
</script>

<style lang="scss" scoped>
.chat-submit {
  &__form {
    display: flex;
    span {
      flex: 1 1 auto;
    }
    ::v-deep textarea {
      resize: none !important;
    }
  }
}

// ::v-deep .CodeMirror,
// ::v-deep.CodeMirror-scroll {
//   min-height: 200px;
// }
</style>
