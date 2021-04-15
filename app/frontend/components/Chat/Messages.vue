<template>
  <div class="messages">
    <template v-if="messages">
      <div
        v-for="message in messages"
        :key="message.id"
        class="message"
        :class="[message.incoming ? 'message--incoming' : 'message--outcoming']"
      >
        <div class="message__wrapper">
          <div class="message__content">{{ message.content }}</div>
          <div class="message__time">{{ message.time }}</div>
        </div>
      </div>
    </template>

    <div v-else class="messages__loader">
      <UiLoader :loading="true" theme="block" />
    </div>
  </div>
</template>

<script>
export default {
  name: 'ChatMessages',
  props: {
    messages: Array,
  },
};
</script>

<style lang="scss" scoped>
.messages {
  position: relative;
  flex: 1 0 auto;
  display: flex;
  flex-direction: column;
  justify-content: flex-end;
  padding: 24px;
  // &__loader {

  // }
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
    padding-right: 24px;
  }
  &--outcoming {
    justify-content: flex-start;
    padding-left: 24px;
    .message__wrapper {
      background: #1e88e5;
      color: white;
    }
  }
}

@include r($sm) {
  .messages {
    padding: 16px;
  }
}
</style>
