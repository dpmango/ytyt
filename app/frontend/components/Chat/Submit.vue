<template>
  <div class="chat-submit">
    <ValidationObserver
      ref="form"
      v-slot="{ invalid }"
      tag="form"
      class="chat-submit__form"
      @submit.prevent="handleSubmit"
    >
      <ValidationProvider v-slot="{ errors }" rules="required">
        <UiInput
          textarea
          :value="text"
          rows="1"
          placeholder="Сообщение.."
          :error="errors[0]"
          icon="paper-clip"
          icon-position="left"
          @onChange="(v) => (text = v)"
        />
      </ValidationProvider>
    </ValidationObserver>
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
</style>
