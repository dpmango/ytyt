<template>
  <div v-if="!user.email_confirmed" class="notification">
    <div class="container notification__wrapper">
      <span class="notification__message">
        На <strong>{{ user.email }}</strong> было отправлено письмо. Пожалуйста, откройте его и перейдите по ссылке,
        чтобы завершить регистрацию.
        <a class="notification__cta" @click="handleClick"> Отправить письмо еще раз </a>
      </span>
    </div>
  </div>
</template>

<script>
import { mapActions, mapGetters } from 'vuex';

export default {
  computed: {
    ...mapGetters('auth', ['user']),
  },
  methods: {
    handleClick() {
      this.verifyPost()
        .then((res) => {
          this.$toast.global.default({ message: res.detail });
        })
        .catch((err) => {
          this.$toast.global.error({ message: err.data });
        });
    },
    ...mapActions('auth', ['verifyPost']),
  },
};
</script>

<style lang="scss" scoped>
.notification {
  position: relative;
  z-index: 2;
  background: rgba(#38bff2, 0.1);
  &__wrapper {
    display: flex;
    align-items: center;
    padding-top: 10px;
    padding-bottom: 10px;
  }
  &__message {
    font-size: 15px;
  }
  &__cta {
    color: $colorPrimary;
    transition: color 0.25s $ease;
    cursor: pointer;
    &:hover {
      color: $fontColor;
    }
  }
}

@include r($sm) {
  .notification {
    &__wrapper {
      padding-left: 16px;
      padding-right: 16px;
    }
  }
}
</style>
