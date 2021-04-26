<template>
  <ChatHome />
</template>

<script>
export default {
  head: {
    title: 'Сообщения',
  },
  mounted() {
    if (!this.$store.getters['chat/isConnected']) {
      this.$store.dispatch('chat/connect');
    }
  },
};
</script>
