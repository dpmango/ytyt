<template>
  <div v-if="!user.email_confirmed" class="notification">
    <div class="notification__wrapper">
      <span class="notification__message">
        Пожалуйста подтвердите адрес электронной почты,
        <a class="notification__cta" @click="handleClick"> отправить ссылку еще раз </a>
      </span>
    </div>
  </div>
</template>

<script>
import { mapGetters } from 'vuex';

export default {
  computed: {
    ...mapGetters('auth', ['user']),
  },
  methods: {
    handleClick() {
      alert('Нужен метод на API');
    },
  },
};
</script>

<style lang="scss" scoped>
.notification {
  position: relative;
  z-index: 2;
  &__wrapper {
    display: flex;
    align-items: center;
    border-radius: 0;
    margin: 0;
    background: rgba($colorRed, 0.1);
    padding: 10px 32px;
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
