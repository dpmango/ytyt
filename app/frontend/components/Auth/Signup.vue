<template>
  <AuthWrapper>
    <template #title>Регистрация</template>

    <template #actions>
      <NuxtLink to="/auth/login">Войти</NuxtLink>
    </template>

    <template #form>
      <ValidationObserver ref="form" v-slot="{ invalid }" tag="form" class="login__form" @submit.prevent="handleSubmit">
        <UiError :error="error" />

        <ValidationProvider v-slot="{ errors }" rules="required">
          <UiInput
            :value="firstName"
            theme="dynamic"
            name="firstName"
            label="Имя"
            type="text"
            :error="errors[0]"
            @onChange="(v) => (firstName = v)"
          />
        </ValidationProvider>
        <UiInput
          :value="lastName"
          theme="dynamic"
          name="lastName"
          label="Фамилия"
          type="text"
          @onChange="(v) => (lastName = v)"
        />
        <ValidationProvider v-slot="{ errors }" rules="email|required">
          <UiInput
            :value="email"
            theme="dynamic"
            name="email"
            label="Email"
            type="email"
            :error="errors[0]"
            @onChange="(v) => (email = v)"
          />
        </ValidationProvider>
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
            theme="dynamic"
            :value="passwordConfirm"
            name="password"
            label="Повторите Пароль"
            type="password"
            :error="errors[0]"
            @onChange="(v) => (passwordConfirm = v)"
          />
        </ValidationProvider>
        <UiButton type="submit" block>Зарегистрироваться</UiButton>
      </ValidationObserver>
    </template>
  </AuthWrapper>
</template>

<script>
import { mapActions } from 'vuex';
import { rebuildSocket } from '~/helpers/RebuildSocket';

export default {
  data() {
    return {
      firstName: null,
      lastName: null,
      email: null,
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
      const { firstName, lastName, email, password, passwordConfirm } = this;
      await this.signup({
        first_name: firstName,
        last_name: lastName,
        email,
        password1: password,
        password2: passwordConfirm,
      })
        .then((_res) => {
          this.verifyPost();
          this.error = null;
          rebuildSocket(this);
          this.$router.push('/course');
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
    ...mapActions('auth', ['signup', 'verifyPost']),
  },
};
</script>
