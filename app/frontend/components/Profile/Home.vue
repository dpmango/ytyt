<template>
  <div class="profile">
    <div class="container">
      <div class="profile__wrapper">
        <div class="profile__box">
          <div class="row profile__box-wrapper">
            <div class="profile__avatar">
              <div class="profile__avatar-image">
                <img :src="avatarBlob || avatar" />
                <div class="profile__avatar-uploader">
                  <UiUploader
                    :file="avatarFile"
                    :allowed-mime="['image']"
                    :max-size="5"
                    :include-reader="true"
                    @onReader="(img) => (avatarBlob = img)"
                    @onChange="(f) => (avatarFile = f)"
                    @handleError="(err) => (avatarError = err)"
                  >
                    <template #info="slotProps">
                      <span v-if="slotProps.file">{{ slotProps.file.name }}</span>
                    </template>
                    <template #error="slotProps">
                      <span v-if="slotProps.error">{{ slotProps.error }}</span>
                    </template>
                    <template #button="slotProps">
                      <div class="profile__avatar-uploader-trigger" @click="slotProps.trigger">
                        <UiSvgIcon name="camera" />
                      </div>
                    </template>
                  </UiUploader>
                </div>
              </div>

              <div v-if="avatarError" class="profile__avatar-error">
                <div class="profile__avatar-error-icon">
                  <UiSvgIcon name="paper-clip" />
                </div>
                <span class="profile__avatar-error-name">{{ avatarError }}</span>
              </div>
            </div>
            <div class="profile__content">
              <client-only>
                <template slot="placeholder">
                  <UiLoader :loading="true" theme="block" />
                </template>

                <ValidationObserver
                  ref="form"
                  v-slot="{ invalid }"
                  tag="form"
                  class="profile__form"
                  @submit.prevent="handleSubmit"
                >
                  <UiError :error="error" />

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
                      placeholder="Replit"
                      icon="repl"
                      icon-position="left"
                      @onChange="(v) => (github = v)"
                    />
                  </ValidationProvider>

                  <UiToggle
                    label="Отправлять уведомления о новых сообщениях на email"
                    :value="notifications"
                    @onChange="(val) => (notifications = val)"
                  />

                  <UiButton :is-loading="isLoading" type="submit" block>Сохранить изменения</UiButton>
                  <NuxtLink to="/profile/password">
                    <UiButton theme="outline" block>Сменить пароль</UiButton>
                  </NuxtLink>
                </ValidationObserver>
              </client-only>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { mapActions, mapGetters } from 'vuex';

export default {
  props: {},
  data() {
    return {
      isLoading: false,
      email: null,
      name: null,
      github: null,
      avatar: null,
      notifications: null,
      avatarFile: null,
      avatarBlob: null,
      avatarError: null,
    };
  },
  computed: {
    ...mapGetters('auth', ['user']),
  },
  created() {
    this.getUser();
  },
  methods: {
    async getUser() {
      await this.getUserInfo()
        .then((res) => {
          this.setUserInfo();
        })
        .catch((_err) => {});
    },
    setUserInfo() {
      const clear = (x) => x || '';
      const user = this.user;

      this.email = user.email;
      this.name = `${clear(user.first_name)} ${clear(user.middle_name)} ${clear(user.last_name)}`.trim();
      this.github = user.github_url;
      this.avatar = user.avatar;
      this.notifications = user.email_notifications;
    },
    async handleSubmit() {
      const isValid = await this.$refs.form.validate();
      if (!isValid) {
        return;
      }

      const { email, name, notifications, github, avatarFile } = this;

      const formatName = (str) => {
        const split = str.split(' ');
        let [first, last] = [null, null];

        if (split.length > 1) {
          [first, last] = split;
        } else {
          first = split;
        }

        return {
          first_name: first,
          last_name: last,
        };
      };

      const { first_name, middle_name, last_name } = formatName(name);

      // build form data with optional avatar image
      const formData = new FormData();
      formData.append('email', email);
      formData.append('email_notifications', notifications);
      if (first_name) {
        formData.append('first_name', first_name);
      }
      if (middle_name) {
        formData.append('middle_name', middle_name);
      }
      if (last_name) {
        formData.append('last_name', last_name);
      }
      if (github) {
        formData.append('github_url', github);
      }

      if (this.avatarFile) {
        formData.append('avatar', avatarFile);
      }

      this.isLoading = true;

      await this.startUpadte(formData);

      this.isLoading = false;
    },
    async startUpadte(formData) {
      await this.update(formData)
        .then((_res) => {
          this.error = null;
          // this.avatarBlob = null;
          this.$toast.global.default({ message: 'Изменения сохранены' });
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
    ...mapActions('auth', ['getUserInfo', 'update']),
  },
};
</script>

<style lang="scss" scoped>
.profile {
  padding-top: 24px;
  padding-bottom: 24px;
  &__wrapper {
    display: flex;
  }
  &__box {
    flex: 0 1 654px;
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
    > .svg-icon {
      position: absolute;
      z-index: 2;
      top: 50%;
      left: 50%;
      transform: translate(-50%, -50%);
      font-size: 64px;
      color: $colorGray;
    }
    ::v-deep .uploader {
      flex: 1 0 auto;
      display: flex;
      flex-direction: column;
      .uploader__wrapper {
        flex: 1 0 auto;
        display: flex;
        flex-direction: column;
        align-items: stretch;
      }
    }
  }
  &__avatar-uploader {
    position: absolute;
    z-index: 2;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    display: flex;
    flex-direction: column;
    background: rgba($fontColor, 0.3);
    color: rgba(white, 0.8);
    // hides all info && error
    font-size: 0;
    opacity: 0;
    transition: opacity 0.25s $ease;
    &:hover {
      opacity: 1;
    }
    .svg-icon {
      font-size: 28px;
    }
  }
  &__avatar-uploader-trigger {
    flex: 1 0 auto;
    display: flex;
    justify-content: center;
    align-items: center;
  }
  &__avatar-error {
    margin-top: 16px;
    display: flex;
    align-items: center;
    min-height: 36px;
    color: $colorRed;
  }
  &__avatar-error-icon {
    flex: 0 0 auto;
    font-size: 0;
    .svg-icon {
      font-size: 16px;
    }
  }
  &__avatar-error-name {
    display: inline-block;
    margin-left: 8px;
    font-size: 14px;
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
      &.outline {
        margin-top: 10px;
      }
    }
  }
}

@include r($lg) {
  .profile {
    &__wrapper {
      flex-wrap: wrap;
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
