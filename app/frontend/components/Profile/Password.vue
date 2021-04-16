<template>
  <AuthWrapper>
    <template #title>Смените пароль</template>

    <template #actions>
      <NuxtLink to="/profile">Вернуться</NuxtLink>
    </template>

    <template #form>
      <ValidationObserver ref="form" v-slot="{ invalid }" tag="form" class="login__form" @submit.prevent="handleSubmit">
        <UiError :error="error" />
        <ValidationProvider v-slot="{ errors }" rules="required|min:8" vid="password">
          <UiInput
            :value="passwordCurrent"
            name="password"
            label="Старый Пароль"
            type="password"
            :error="errors[0]"
            @onChange="(v) => (passwordCurrent = v)"
          />
        </ValidationProvider>
        <ValidationProvider v-slot="{ errors }" rules="required|min:8" vid="password">
          <UiInput
            :value="password"
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
      passwordCurrent: null,
      password: null,
      passwordConfirm: null,
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

      await this.passwordChange({
        old_password: this.passwordCurrent,
        new_password1: this.password,
        new_password2: this.passwordConfirm,
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
    ...mapActions('auth', ['passwordChange']),
  },
};
</script>
