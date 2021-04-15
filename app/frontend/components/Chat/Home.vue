<template>
  <div class="chat">
    <div class="chat__wrapper" :class="[activeDialog && 'is-dialog-active']">
      <div class="chat__sidebar">
        <ChatDialogs :dialogs="dialogs" :active-dialog="activeDialog" :set-dialog="setDialog" />
      </div>

      <div class="chat__content">
        <div class="chat__head">
          <ChatHead :click-back="handleClickBack" :data="head" />
        </div>
        <div class="chat__dialog">
          <ChatMessages :messages="messages" />
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
  data() {
    return {
      activeDialog: null,
    };
  },
  computed: {
    ...mapGetters('chat', ['messages', 'head', 'dialogs']),
  },
  created() {
    // sockets ws:
    // this.handleTestGetUser();
  },
  methods: {
    setDialog(id) {
      this.activeDialog = id;
    },
    handleClickBack() {
      this.activeDialog = null;
    },
    async handleSubmit() {
      const isValid = await this.$refs.form.validate();
    },
    // ...mapActions('auth', ['logout', 'getUserInfo', 'update']),
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

@include r($md) {
  .chat {
    &__wrapper {
      will-change: transform;
      transition: transform 0.3s $ease;
      &.is-dialog-active {
        transform: translateX(-50%);
        .chat__content {
          transform: translateX(-50%);
        }
      }
    }
    &__sidebar {
      z-index: 2;
      flex-basis: 100%;
      max-width: 100%;
    }
    &__content {
      z-index: 3;
      flex-basis: 100%;
      max-width: 100%;
      will-change: transform;
      transition: transform 0.25s ease-in;
    }
  }
}
</style>
