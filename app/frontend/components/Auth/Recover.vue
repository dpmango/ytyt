<template>
  <AuthWrapper>
    <template #title>Восстановить пароль</template>

    <template #actions>
      <NuxtLink to="/auth/login">Войти</NuxtLink>
    </template>

    <template #form>
      <ValidationObserver ref="form" v-slot="{ invalid }" tag="form" class="login__form" @submit.prevent="handleSubmit">
        <UiError :error="error" />

        <ValidationProvider v-slot="{ errors }" class="ui-group" rules="email|required">
          <UiInput
            :value="email"
            theme="dynamic"
            label="Email"
            type="email"
            :error="errors[0]"
            @onChange="(v) => (email = v)"
          />
        </ValidationProvider>

        <UiButton type="submit" block>Отправить новый пароль</UiButton>
      </ValidationObserver>
    </template>
  </AuthWrapper>
</template>

<script>
import { mapActions } from 'vuex';

export default {
  data() {
    return {
      email: null,
      error: null,
    };
  },
  computed: {},
  methods: {
    async handleSubmit() {
      const isValid = await this.$refs.form.validate();
      if (!isValid) {
        return;
      }

      await this.recover({ email: this.email })
        .then((res) => {
          this.error = null;
          this.$toast.global.default({ message: res.detail });
          this.$router.push('/auth/login');
        })
        .catch((err) => {
          const { data, code } = err;

          if (data && code === 400) {
            Object.keys(data).forEach((key) => {
              this.error = data[key][0];
            });
          }
          if (data && code === 404) {
            this.error = data.detail;
          }
        });
    },
    ...mapActions('auth', ['recover']),
  },
};
</script>
