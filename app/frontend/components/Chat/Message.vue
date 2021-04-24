<template>
  <div class="message" :class="[isIncoming ? 'message--incoming' : 'message--outcoming']">
    <div class="message__wrapper">
      <div class="message__content" v-html="message.body" />
      <div class="message__time">{{ timestamp }}</div>
    </div>
  </div>
</template>

<script>
import { mapGetters } from 'vuex';
import { timeToTimeStamp } from '~/helpers/Date';

export default {
  name: 'ChatMessages',
  props: {
    message: Object,
  },
  computed: {
    isIncoming() {
      return this.message.user.id === this.user.id;
    },
    timestamp() {
      return timeToTimeStamp(this.message.date_created);
    },
    ...mapGetters('auth', ['user']),
  },
};
</script>

<style lang="scss" scoped>
.message {
  margin: 4px 0;
  display: flex;
  &__wrapper {
    position: relative;
    padding: 14px 16px;
    max-width: 440px;
    background: #fff;
    box-shadow: 0 6px 24px -4px rgba(23, 24, 24, 0.1);
    border-radius: 8px;
  }
  &__content {
    font-size: 15px;
    ::v-deep p {
      margin: 0;
      + p {
        margin-top: 1em;
      }
    }
  }
  &__time {
    font-size: 13px;
    text-align: right;
    opacity: 0.5;
  }
  &--incoming {
    justify-content: flex-end;
    // padding-right: 24px;
    .message__wrapper {
      background: #1e88e5;
      color: white;
    }
  }
  &--outcoming {
    justify-content: flex-start;
    // padding-left: 24px;
  }
}
</style>
