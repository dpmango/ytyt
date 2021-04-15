<template>
  <AuthWrapper>
    <template #title>Войти</template>

    <template #actions>
      <NuxtLink to="/auth/signup">Зарегистрироваться</NuxtLink>
      <NuxtLink to="/auth/reset">Забыли пароль?</NuxtLink>
    </template>

    <template #form>
      <ValidationObserver ref="form" v-slot="{ invalid }" tag="form" class="login__form" @submit.prevent="handleSubmit">
        <UiError :error="error" />

        <ValidationProvider v-slot="{ errors }" class="ui-group" rules="email|required">
          <UiInput
            :value="email"
            label="Email"
            placeholder="Email"
            type="email"
            :error="errors[0]"
            @onChange="(v) => (email = v)"
          />
        </ValidationProvider>
        <ValidationProvider v-slot="{ errors }" class="ui-group" rules="required">
          <UiInput
            :value="password"
            label="Пароль"
            type="password"
            :error="errors[0]"
            @onChange="(v) => (password = v)"
          />
        </ValidationProvider>

        <UiButton type="submit" block>Войти</UiButton>
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
      password: null,
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

      const { email, password } = this;
      await this.login({ email, password })
        .then((_res) => {
          this.error = null;
          this.$router.push('/');
        })
        .catch((err) => {
          const { data, code } = err;

          if (data && code === 401) {
            Object.keys(data).forEach((key) => {
              this.error = data[key];
            });
          }
        });
    },
    ...mapActions('auth', ['login']),
  },
};
</script>
