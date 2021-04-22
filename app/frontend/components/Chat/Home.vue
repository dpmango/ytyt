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
    <div v-if="!socket.isConnected" class="chat__loader">
      <UiLoader theme="block" :loading="true" />
    </div>
  </div>
</template>

<script>
import Vue from 'vue';
import { mapActions, mapGetters } from 'vuex';

export default {
  props: {},
  data() {
    return {
      activeDialog: null,
    };
  },
  computed: {
    ...mapGetters('chat', ['messages', 'head', 'dialogs', 'socket']),
  },
  mounted() {
    this.connect();
  },
  beforeDestroy() {
    this.disconnect();
  },
  methods: {
    setDialog(id) {
      this.activeDialog = id;
      // console.log(this.$socket);
    },
    handleClickBack() {
      this.activeDialog = null;
    },
    async handleSubmit() {
      const isValid = await this.$refs.form.validate();
    },
    ...mapActions('chat', ['connect', 'disconnect']),
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
    border-right: 1px solid rgba(147, 149, 152, 0.2);
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
  &__loader {
    position: absolute;
    z-index: 5;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    display: flex;
    align-items: center;
    justify-content: center;
    background: rgba(white, 0.5);
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
