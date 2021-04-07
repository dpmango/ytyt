<template>
  <div class="login">
    <div class="login__title h2-title">Восстановить пароль</div>
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

        <UiButton type="submit" block>Отправить новый пароль</UiButton>
      </ValidationObserver>
    </client-only>

    <div class="login__actions">
      <NuxtLink to="/auth/login">Войти</NuxtLink>
    </div>
  </div>
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
          this.$toast.success(res.detail);
          this.$router.push('/auth/login');
        })
        .catch((err) => {
          const { data, code } = err;

          if (data && code === 400) {
            Object.keys(data).forEach((key) => {
              this.error = data[key][0];
            });
          }
        });
    },
    ...mapActions('auth', ['recover']),
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
