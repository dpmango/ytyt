<template>
  <div class="profile">
    <div class="container">
      <div class="profile__box">
        <div class="row profile__box-wrapper">
          <div class="profile__avatar">
            <div class="profile__avatar-image">
              <UiSvgIcon name="github" />
            </div>
          </div>
          <div class="profile__content">
            <ValidationObserver
              ref="form"
              v-slot="{ invalid }"
              tag="form"
              class="profile__form"
              @submit.prevent="handleSubmit"
            >
              <ValidationProvider v-slot="{ errors }" rules="required">
                <UiInput
                  :value="data.name"
                  type="text"
                  placeholder="Имя"
                  :error="errors[0]"
                  icon="name"
                  icon-position="left"
                  @onChange="(v) => (data.name = v)"
                />
              </ValidationProvider>

              <ValidationProvider v-slot="{ errors }" rules="required">
                <UiInput
                  disabled
                  :value="data.email"
                  type="email"
                  placeholder="Email"
                  :error="errors[0]"
                  icon="email"
                  icon-position="left"
                  @onChange="(v) => null"
                />
              </ValidationProvider>

              <ValidationProvider v-slot="{ errors }">
                <UiInput
                  disabled
                  :value="data.github"
                  type="text"
                  placeholder="Github"
                  :error="errors[0]"
                  icon="github"
                  icon-position="left"
                  @onChange="(v) => null"
                />
              </ValidationProvider>
              <UiButton type="submit" block>Сохранить изменения</UiButton>
            </ValidationObserver>
          </div>
          {{ data }}
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { mapActions, mapGetters } from 'vuex';

export default {
  props: {},
  computed: {
    data() {
      const user = this.user();
      const clear = (x) => x || '';

      return {
        email: user.email,
        name: `${clear(user.first_name)} ${clear(user.middle_name)} ${clear(user.last_name)}`.trim(),
        github: '', // TODO - api
        image: '', // TODO - api
      };
    },
  },
  created() {
    this.handleTestGetUser();
  },
  methods: {
    async handleTestGetUser() {
      await this.getUserInfo()
        .then((res) => {})
        .catch((_err) => {});
    },
    async handleSubmit() {
      const isValid = await this.$refs.form.validate();
      if (!isValid) {
        return;
      }

      const {
        data: { email, name },
      } = this;

      const formatName = (str) => {
        const [first, middle, last] = str.split(' ');

        return {
          first_name: first,
          middle_name: middle,
          last_name: last,
        };
      };

      await this.update({ email, ...formatName(name) })
        .then((_res) => {
          this.error = null;
          this.$toast.success('Пользователь обновлен');
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
    async handleLogout() {
      await this.logout()
        .then((res) => {
          this.$toast.success(res.detail);

          this.$router.push('/auth/login');
        })
        .catch((_err) => {});
    },
    ...mapActions('auth', ['logout', 'getUserInfo', 'update']),
    ...mapGetters('auth', ['user']),
  },
};
</script>

<style lang="scss" scoped>
.profile {
  display: block;
  &__box {
    background: #fff;
    border-radius: 8px;
    padding: 32px 24px;
    max-width: 654px;
  }
  &__box-wrapper {
    // row instance
    position: relative;
    align-items: flex-start;
  }
  &__avatar,
  &__content {
    width: 100%;
    min-width: 1px;
    min-height: 0;
    padding: $gutter;
  }
  &__avatar {
    flex: 0 0 calc(200px + 24px);
    max-width: calc(200px + 24px);
  }
  &__avatar-image {
    position: relative;
    z-index: 1;
    padding-bottom: 100%;
    overflow: hidden;
    border-radius: 50%;
    background: $colorBg;
    font-size: 0;
    img {
      position: absolute;
      z-index: 2;
      top: 0;
      left: 0;
      width: 100%;
      height: 100%;
      object-fit: cover;
    }
    .svg-icon {
      position: absolute;
      z-index: 2;
      top: 50%;
      left: 50%;
      transform: translate(-50%, -50%);
      font-size: 64px;
      color: $colorGray;
    }
  }
  &__content {
    flex: 0 0 calc(100% - 200px - 24px);
    max-width: calc(100% - 200px - 24px);
  }

  &__form {
    margin-top: -16px;
    .input {
      margin-top: 16px;
    }
    .button {
      margin-top: 24px;
    }
  }
}
</style>
