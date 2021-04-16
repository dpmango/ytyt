<template>
  <div v-if="!user.email_confirmed" class="notification">
    <div class="container">
      <div class="notification__wrapper">
        <span class="notification__message">Пожалуйста подтвердите адрес почты</span>
        <div class="notification__cta">
          <UiButton theme="success" size="small">Отправить снова</UiButton>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { mapGetters } from 'vuex';

export default {
  computed: {
    ...mapGetters('auth', ['user']),
  },
  methods: {},
};
</script>

<style lang="scss" scoped>
.notification {
  position: relative;
  z-index: 2;
  &__wrapper {
    display: flex;
    align-items: center;
    border-radius: 8px;
    margin: 16px 0 8px;
    border: 1px solid $colorRed;
    background: rgba($colorRed, 0.05);
    text-align: center;
    padding: 7px 15px;
  }
  &__message {
    font-size: 14px;
    font-weight: 500;
    padding-right: 20px;
  }
  &__cta {
    flex: 0 0 auto;
    margin-left: auto;
  }
}
</style>
