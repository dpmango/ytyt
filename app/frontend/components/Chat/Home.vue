<template>
  <div class="chat">
    <div class="chat__wrapper" :class="[activeDialog && 'is-dialog-active']">
      <div ref="sidebar" class="chat__sidebar">
        <div v-if="scrollDialogs.isLoading" class="chat__sidebar-loader">
          <UiLoader theme="block" :loading="true" />
        </div>
        <ChatDialogs :dialogs="dialogs" :active-dialog="activeDialog" :set-dialog="setDialog" />
      </div>

      <div class="chat__content">
        <div class="chat__head">
          <ChatHead v-if="head" :click-back="handleClickBack" :head="head" />
        </div>
        <div ref="dialogs" class="chat__dialog">
          <div v-if="scrollMessages.isLoading" class="chat__dialog-loader">
            <UiLoader theme="block" :loading="true" />
          </div>
          <ChatMessages :messages="messages" />
        </div>
        <div class="chat__submit">
          <ChatSubmit v-if="head" @messageSend="messageSend" />
        </div>
      </div>
    </div>
    <div v-if="!isConnected" class="chat__loader">
      <UiLoader theme="block" :loading="true" />
    </div>
  </div>
</template>

<script>
import throttle from 'lodash/throttle';
import { mapActions, mapGetters, mapMutations } from 'vuex';
import { scrollToEnd } from '~/helpers/Scroll';

export default {
  props: {},
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
  },
  watch: {
    activeDialog() {
      // TODO - any alternatives to timeout? (rendering accures a bit later)
      setTimeout(() => {
        scrollToEnd(500, this.$refs.dialogs);
      }, 200);
    },
  },
  created() {
    this.scrollSidebarWithThrottle = throttle(this.handleSidebarScroll, 100);
    this.scrollDialogsWithThrottle = throttle(this.handleDialogScroll, 100);
  },
  mounted() {
    if (this.$refs.sidebar) {
      this.$refs.sidebar.addEventListener('scroll', this.scrollSidebarWithThrottle, false);
    }

    if (this.$refs.dialogs) {
      this.$refs.dialogs.addEventListener('scroll', this.scrollDialogsWithThrottle, false);
    }

    if (!this.isConnected) {
      this.connect();
    }
  },
  beforeDestroy() {
    if (this.$refs.sidebar) {
      this.$refs.sidebar.removeEventListener('scroll', this.scrollSidebarWithThrottle, false);
    }

    if (this.$refs.dialogs) {
      this.$refs.dialogs.removeEventListener('scroll', this.scrollDialogsWithThrottle, false);
    }

    if (this.isConnected) {
      this.disconnect();
    }
  },
  methods: {
    setDialog(id) {
      this.getMessages({ id });
    },
    handleClickBack() {
      this.setActiveDialog(null);
    },
    async handleSidebarScroll() {
      const { scrollHeight, scrollTop, offsetHeight } = this.$refs.sidebar;
      const { lastScroll, direction, isLoading } = this.scrollDialogs;

      const scrollBottom = scrollHeight - scrollTop - offsetHeight;

      if (direction === 'down' && scrollBottom <= 150 && !isLoading) {
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

      if (direction === 'up' && scrollTop <= 150 && !isLoading) {
        const { total, limit, offset } = this.messagesMeta;

        if (total > limit + offset) {
          this.scrollMessages.isLoading = true;
          await this.getMessages({ id: this.activeDialog, offset: offset + limit });
          this.scrollMessages.isLoading = false;
        }
      }

      this.scrollMessages.direction = scrollTop >= lastScroll ? 'down' : 'up';
      this.scrollMessages.lastScroll = scrollTop;
    },
    messageSend() {
      scrollToEnd(500, this.$refs.dialogs);
    },
    ...mapActions('chat', ['connect', 'disconnect', 'getDialogs', 'getMessages']),
    ...mapMutations('chat', ['setActiveDialog']),
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
