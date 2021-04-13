<template>
  <div class="chat">
    <div class="chat__wrapper">
      <div class="chat__sidebar">
        <ChatDialogs />
      </div>

      <div class="chat__content">
        <div class="chat__head">
          <ChatHead />
        </div>
        <div class="chat__dialog">
          <ChatMessages />
        </div>
        <div class="chat__submit">
          <ChatSubmit />
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { mapActions, mapGetters } from 'vuex';

export default {
  props: {},
  computed: {},
  created() {
    // sockets ws:
    // this.handleTestGetUser();
  },
  methods: {
    async handleSubmit() {
      const isValid = await this.$refs.form.validate();
    },
    // ...mapActions('auth', ['logout', 'getUserInfo', 'update']),
    // ...mapGetters('auth', ['user']),
  },
};
</script>

<style lang="scss" scoped>
.chat {
  display: block;
  // &__box {
  // }
  &__wrapper {
    display: flex;
    flex-wrap: wrap;
    position: relative;
  }
  &__sidebar,
  &__content {
    width: 100%;
    min-width: 1px;
    min-height: 0;
    display: flex;
    flex-direction: column;
    height: calc(100vh - 56px);
  }
  &__sidebar {
    position: relative;
    z-index: 3;
    flex: 0 0 294px;
    max-width: 294px;
    background: white;
  }
  &__content {
    position: relative;
    z-index: 2;
    flex: 0 0 calc(100% - 294px);
    max-width: calc(100% - 294px);
    background: #fafafa;
  }

  &__head {
    flex: 0 0 auto;
  }
  &__dialog {
    flex: 0 1 auto;
    display: flex;
    flex-direction: column;
    overflow-y: auto;
    height: 100%;
  }
  &__submit {
    flex: 0 0 auto;
    margin-top: auto;
    background: white;
    box-shadow: 0 0 12px 0 rgba($fontColor, 0.05);
  }
}
</style>
