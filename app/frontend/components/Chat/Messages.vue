<template>
  <div class="messages">
    <template v-if="messages">
      <ChatMessage v-for="message in messages" :key="message.id" :message="message" />
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

@include r($sm) {
  .messages {
    padding: 16px;
  }
}
</style>
