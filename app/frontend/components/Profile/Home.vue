<template>
  <div class="profile">
    <div class="container">
      <div class="profile__box">
        <div class="row profile__box-wrapper">
          <div class="profile__avatar">
            <div class="profile__avatar-image">
              <img :src="avatar" />
            </div>
            <UiUploader
              :file="avatarFile"
              :allowed-mime="['image', 'application']"
              :max-size="5"
              @onChange="(f) => (avatarFile = f)"
            />
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
                  :value="name"
                  type="text"
                  placeholder="Имя"
                  :error="errors[0]"
                  icon="name"
                  icon-position="left"
                  @onChange="(v) => (name = v)"
                />
              </ValidationProvider>

              <ValidationProvider v-slot="{ errors }" rules="required">
                <UiInput
                  disabled
                  :value="email"
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
                  :value="github"
                  type="text"
                  placeholder="Github"
                  :error="errors[0]"
                  icon="github"
                  icon-position="left"
                  @onChange="(v) => (github = v)"
                />
              </ValidationProvider>

              <UiToggle
                label="Отправлять уведомления о новых сообщениях на email"
                :value="notifications"
                @onChange="(val) => (notifications = val)"
              />

              <UiButton type="submit" block>Сохранить изменения</UiButton>
            </ValidationObserver>
          </div>
        </div>
      </div>
      <div class="mt-1">
        <UiButton theme="danger" @click="handleLogout">Выйти</UiButton>
      </div>
    </div>
  </div>
</template>

<script>
import { mapActions, mapGetters } from 'vuex';

export default {
  props: {},
  data() {
    const user = this.user();
    const clear = (x) => x || '';

    return {
      email: user.email,
      name: `${clear(user.first_name)} ${clear(user.middle_name)} ${clear(user.last_name)}`.trim(),
      github: user.github_url,
      avatar: user.avatar,
      notifications: user.email_notifications,
      avatarFile: undefined,
    };
  },
  computed: {},
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

      const { email, name, notifications, github } = this;

      const formatName = (str) => {
        const [first, middle, last] = str.split(' ');

        return {
          first_name: first,
          middle_name: middle,
          last_name: last,
        };
      };

      const patchObject = { email, ...formatName(name), email_notifications: notifications, github_url: github };

      await this.update(patchObject)
        .then((_res) => {
          this.error = null;
          this.$toast.global.success({ message: 'Пользователь обновлен' });
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
          this.$toast.global.success({ message: res.detail });

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
  padding-top: 24px;
  padding-bottom: 24px;
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
    .toggle {
      margin-top: 24px;
    }
    .button {
      margin-top: 24px;
    }
  }
}

@include r($md) {
  .profile {
    background: white;
    &__box {
      max-width: 100%;
      background: transparent;
      padding: 0;
    }
    &__avatar,
    &__content {
      flex: 0 0 100%;
      max-width: 100%;
    }
    &__avatar {
      display: flex;
      justify-content: center;
    }
    &__avatar-image {
      width: 154px;
      height: 154px;
      margin-left: auto;
      margin-right: auto;
      padding-bottom: 0;
    }
  }
}
</style>
