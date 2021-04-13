<template>
  <div class="login">
    <div class="login__title h2-title">Вход</div>
    <client-only>
      <template slot="placeholder">
        <UiLoader :loading="true" theme="block" />
      </template>
      <ValidationObserver ref="form" v-slot="{ invalid }" tag="form" class="login__form" @submit.prevent="handleSubmit">
        <UiError :error="error" />

        <ValidationProvider v-slot="{ errors }" rules="email|required">
          <UiInput
            :value="email"
            label="Email"
            placeholder="Email"
            type="email"
            :error="errors[0]"
            @onChange="(v) => (email = v)"
          />
        </ValidationProvider>
        <ValidationProvider v-slot="{ errors }" rules="required">
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
    </client-only>

    <div class="login__actions">
      <NuxtLink to="/auth/signup">Зарегистрироваться</NuxtLink>
      <NuxtLink to="/auth/recover">Забыли пароль?</NuxtLink>
    </div>
  </div>
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

<style lang="scss" scoped>
.login {
  max-width: 400px;
  margin: 0 auto;
  padding: 36px 20px;
  &__title {
    text-align: center;
  }
  &__form {
    margin-top: 24px;
    .input {
      margin-top: 16px;
    }
    .button {
      margin-top: 24px;
    }
  }
  &__actions {
    margin-top: 20px;
    font-size: 15px;
    line-height: 1.5;
    text-align: center;
    a {
      position: relative;
      color: $colorPrimary;
      &::after {
        display: inline-block;
        content: '|';
        color: rgba(23, 24, 24, 0.3);
        margin: 0 2px 0 6px;
      }
      &:last-child {
        &::after {
          display: none;
        }
      }
    }
  }
}
</style>
