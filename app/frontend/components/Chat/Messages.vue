<template>
  <div class="messages">
    <div
      v-for="message in list"
      :key="message.id"
      class="message"
      :data-id="message.id"
      :class="[message.incoming ? 'message--incoming' : 'message--outcoming']"
      ]
    >
      <div class="message__wrapper">
        <div class="message__content">{{ message.content }}</div>
        <div class="message__time">{{ message.time }}</div>
      </div>
    </div>
  </div>
</template>

<script>
import { mapActions, mapGetters } from 'vuex';
import { MESSAGES_TEST_DATA } from './helpers/mockData';

export default {
  props: {},
  data() {
    return {
      list: MESSAGES_TEST_DATA,
    };
  },
  computed: {},
  methods: {
    // ...mapActions('auth', ['logout', 'getUserInfo', 'update']),
    // ...mapGetters('auth', ['user']),
  },
};
</script>

<style lang="scss" scoped>
.messages {
  flex: 1 0 auto;
  display: flex;
  flex-direction: column;
  justify-content: flex-end;
  padding: 24px;
}

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
  }
  &__time {
    font-size: 13px;
    text-align: right;
    opacity: 0.5;
  }
  &--incoming {
    justify-content: flex-end;
  }
  &--outcoming {
    justify-content: flex-start;
    .message__wrapper {
      background: #1e88e5;
      color: white;
    }
  }
}
</style>
