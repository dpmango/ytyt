<template>
  <div class="chat" :class="[isMini && 'is-mini', isMiniOpened && 'is-mini-opened']">
    <div class="container">
      <div class="chat__wrapper" :class="[activeDialog && 'is-dialog-active']">
        <div ref="sidebar" class="chat__sidebar">
          <div v-if="scrollDialogs.isLoading" class="chat__sidebar-loader">
            <UiLoader theme="block" :loading="true" />
          </div>
          <ChatDialogs :dialogs="dialogs" :active-dialog="activeDialog" :set-dialog="setDialog" />
        </div>

        <div class="chat__content">
          <div v-if="socket.error || socket.reconnectError" class="chat__error">
            <p>{{ socket.error || 'Возникала ошибка. Попробуйте обновить' }}</p>
            <UiButton size="small" theme="success" @click="rebuildSocket">Обновить</UiButton>
          </div>
          <div class="chat__head">
            <ChatHead v-if="head" :click-back="handleClickBack" :click-back-mini="handleClickBackMini" :head="head" />
          </div>
          <div ref="dialogs" class="chat__dialog">
            <div v-if="scrollMessages.isLoading" class="chat__dialog-loader">
              <UiLoader theme="block" :loading="true" />
            </div>
            <ChatMessages :messages="messages" />
          </div>
          <div class="chat__submit">
            <ChatSubmit v-if="head" @onSubmit="scrollDialogsToBottom" />
          </div>
        </div>
      </div>
      <div v-if="!isConnected" class="chat__loader">
        <UiLoader theme="block" :loading="true" />
      </div>
    </div>
  </div>
</template>

<script>
import throttle from 'lodash/throttle';
import { mapActions, mapGetters, mapMutations } from 'vuex';
import { scrollToEnd } from '~/helpers/Scroll';
import { rebuildSocket } from '~/helpers/RebuildSocket';

export default {
  props: {
    isMini: Boolean,
    isMiniOpened: Boolean,
    handleClickBackMini: Function,
  },
  data() {
    return {
      scrollDialogs: {
        lastScroll: null,
        direction: null,
        isLoading: false,
      },
      scrollMessages: {
        lastScroll: null,
        direction: null,
        isLoading: false,
      },
    };
  },
  computed: {
    ...mapGetters('chat', [
      'activeDialog',
      'dialogs',
      'head',
      'messages',
      'messagesMeta',
      'dialogsMeta',
      'socket',
      'isConnected',
    ]),
    ...mapGetters('auth', ['user']),
  },
  watch: {
    isConnected() {
      if (this.isMini && this.user.dialog && this.isConnected) {
        this.setDialog(parseInt(this.user.dialog.id));
      }
    },
    messages(newVal, oldVal) {
      const { scrollTop, scrollHeight, offsetHeight } = this.$refs.dialogs;
      const scrollBottom = scrollHeight - scrollTop - offsetHeight;

      // prevent scrolling if user reading prev. messages or new messages loaded on 'up' scroll
      if (scrollBottom <= 50 && !(oldVal.length === 0)) {
        scrollToEnd(500, this.$refs.dialogs);
      }

      // check read status if no scroll height (scroll event wont be triggered)
      if (scrollHeight <= offsetHeight) {
        setTimeout(() => {
          this.readMessages();
        }, 200);
        setTimeout(() => {
          this.readMessages();
        }, 500);
      }
    },
  },
  created() {
    this.scrollSidebarWithThrottle = throttle(this.handleSidebarScroll, 300);
    this.scrollDialogsWithThrottle = throttle(this.handleDialogScroll, 300);
  },
  mounted() {
    if (this.$refs.sidebar) {
      this.$refs.sidebar.addEventListener('scroll', this.scrollSidebarWithThrottle, false);
    }

    if (this.$refs.dialogs) {
      this.$refs.dialogs.addEventListener('scroll', this.scrollDialogsWithThrottle, false);
    }

    if (this.$route.query && this.$route.query.id && this.isConnected) {
      this.setDialog(parseInt(this.$route.query.id));
    }

    if (this.isMini && this.user.dialog && this.isConnected) {
      this.setDialog(parseInt(this.user.dialog.id));
    }
  },
  beforeDestroy() {
    if (this.$refs.sidebar) {
      this.$refs.sidebar.removeEventListener('scroll', this.scrollSidebarWithThrottle, false);
    }

    if (this.$refs.dialogs) {
      this.$refs.dialogs.removeEventListener('scroll', this.scrollDialogsWithThrottle, false);
    }
  },
  methods: {
    async setDialog(id) {
      await this.getMessages({ id });
      this.setActiveDialog(id);
      setTimeout(() => {
        scrollToEnd(0, this.$refs.dialogs);
      }, 200);
    },
    handleClickBack() {
      if (this.isMini) {
        this.handleClickBackMini();
      } else {
        this.resetMessages();
      }
    },

    async handleSidebarScroll() {
      const { scrollHeight, scrollTop, offsetHeight } = this.$refs.sidebar;
      const { lastScroll, direction, isLoading } = this.scrollDialogs;

      const scrollBottom = scrollHeight - scrollTop - offsetHeight;

      if (direction === 'down' && scrollBottom <= 250 && !isLoading) {
        const { total, limit, offset } = this.dialogsMeta;

        if (total > limit + offset) {
          this.scrollDialogs.isLoading = true;
          await this.getDialogs({ offset: offset + limit });
          this.scrollDialogs.isLoading = false;
        }
      }

      this.scrollDialogs.direction = scrollTop >= lastScroll ? 'down' : 'up';
      this.scrollDialogs.lastScroll = scrollTop;
    },
    async handleDialogScroll() {
      const { scrollTop } = this.$refs.dialogs;
      const { lastScroll, direction, isLoading } = this.scrollMessages;

      if (direction === 'up' && scrollTop <= 250 && !isLoading) {
        const { total, limit, offset } = this.messagesMeta;

        if (total > limit + offset) {
          this.scrollMessages.isLoading = true;
          await this.getMessages({ id: this.activeDialog, offset: offset + limit });
          this.scrollMessages.isLoading = false;
        }
      }

      this.scrollMessages.direction = scrollTop >= lastScroll ? 'down' : 'up';
      this.scrollMessages.lastScroll = scrollTop;

      this.readMessages();
    },
    readMessages() {
      if (!this.$refs.sidebar) return;
      const { offsetHeight } = this.$refs.sidebar;
      const dialogsTop = this.$refs.dialogs.getBoundingClientRect().top;
      const messages = this.$refs.dialogs.querySelectorAll('.message--outcoming[data-read="false"]');

      if (!messages) return;

      messages.forEach((message) => {
        const rect = message.getBoundingClientRect();
        const isVisible = rect.top - dialogsTop >= 0 && rect.top - rect.height <= offsetHeight;
        const isSupportMessage = message.getAttribute('data-support') === 'true' && this.user.is_support;
        if (isVisible && !isSupportMessage) {
          this.readMessage({
            dialog_id: this.activeDialog,
            message_id: message.getAttribute('data-id'),
          });
        }
      });
    },
    rebuildSocket() {
      rebuildSocket(this);
    },
    scrollDialogsToBottom() {
      scrollToEnd(500, this.$refs.dialogs);
    },
    ...mapActions('chat', ['connect', 'disconnect', 'getDialogs', 'getMessages', 'readMessage']),
    ...mapMutations('chat', ['setActiveDialog', 'resetMessages']),
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
    overflow-y: auto;
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
    position: relative;
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
  &__dialog-loader {
    position: absolute;
    z-index: 5;
    top: 0;
    left: 50%;
    transform: translateX(-50%);
  }
  &__sidebar-loader {
    position: absolute;
    z-index: 5;
    bottom: 0;
    left: 50%;
    transform: translateX(-50%);
  }
  &__error {
    position: absolute;
    z-index: 6;
    top: 84px;
    left: 24px;
    right: 24px;
    padding: 7px 15px;
    display: flex;
    align-items: center;
    border: 2px solid $colorRed;
    background: white;
    border-radius: 8px;
    p {
      font-size: 15px;
      font-weight: 500;
      margin: 0 10px 0 0;
    }
    .button {
      margin-left: auto;
    }
  }
}

@include r($md) {
  .chat:not(.is-mini) {
    .chat__wrapper {
      will-change: transform;
      transition: transform 0.3s $ease;
      &.is-dialog-active {
        transform: translateX(-50%);
        .chat__content {
          transform: translateX(-50%);
        }
      }
    }
    .container {
      padding-left: 0;
      padding-right: 0;
    }
    .chat__sidebar {
      z-index: 2;
      flex-basis: 100%;
      max-width: 100%;
    }
    .chat__content {
      z-index: 3;
      flex-basis: 100%;
      max-width: 100%;
      will-change: transform;
      transition: transform 0.25s ease-in;
    }
  }
}

// mini chat
.chat.is-mini {
  position: fixed;
  z-index: 999;
  top: 0;
  right: 0;
  bottom: 0;
  width: 100%;
  max-width: 50%;
  box-shadow: 0 6px 24px -4px rgba(23, 24, 24, 0.1);
  transform: translate(100%, 0);
  pointer-events: none;
  transition: transform 0.25s $ease;
  .container {
    padding-left: 0;
    padding-right: 0;
  }
  &.is-mini-opened {
    transform: none;
    pointer-events: all;
  }
  .chat {
    &__wrapper {
      display: block;
    }
    &__sidebar {
      display: none;
    }
    &__content {
      flex-basis: 100%;
      max-width: 100%;
      height: 100vh;
      padding-top: 0;
      background: #fafafa;
      .messages {
        padding-left: 16px;
        padding-right: 16px;
      }
    }
  }
}

@include r($md) {
  .chat.is-mini {
    max-width: 100%;
    ::v-deep .head__mini-close {
      display: none;
    }
  }
}
</style>
