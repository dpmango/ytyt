<template>
  <AuthWrapper>
    <template #title>Смените пароль</template>

    <template #actions>
      <NuxtLink to="/auth/login">Войти</NuxtLink>
    </template>

    <template #form>
      <ValidationObserver ref="form" v-slot="{ invalid }" tag="form" class="login__form" @submit.prevent="handleSubmit">
        <UiError :error="error" />

        <ValidationProvider v-slot="{ errors }" rules="required|min:8" vid="password">
          <UiInput
            :value="password"
            theme="dynamic"
            name="password"
            label="Пароль"
            type="password"
            :error="errors[0]"
            @onChange="(v) => (password = v)"
          />
        </ValidationProvider>
        <ValidationProvider v-slot="{ errors }" rules="required|confirmed:password">
          <UiInput
            :value="passwordConfirm"
            theme="dynamic"
            name="password"
            label="Повторите Пароль"
            type="password"
            :error="errors[0]"
            @onChange="(v) => (passwordConfirm = v)"
          />
        </ValidationProvider>

        <UiButton type="submit" block>Сменить пароль</UiButton>
      </ValidationObserver>
    </template>
  </AuthWrapper>
</template>

<script>
import { mapActions } from 'vuex';

export default {
  data() {
    return {
      password: null,
      passwordConfirm: null,
      query: null,
      error: null,
    };
  },
  computed: {},
  created() {
    // store in state is much safer
    this.query = this.$route.query;
  },
  methods: {
    async handleSubmit() {
      const isValid = await this.$refs.form.validate();
      if (!isValid) {
        return;
      }

      await this.recoverConfirmation({
        ...{ new_password1: this.password, new_password2: this.passwordConfirm },
        ...this.query,
      })
        .then((res) => {
          this.error = null;
          this.$toast.global.success({ message: res.detail });
          this.$router.push('/profile');
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
    ...mapActions('auth', ['recoverConfirmation']),
  },
};
</script>
