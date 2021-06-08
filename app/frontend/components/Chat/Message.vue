<template>
  <div
    class="message"
    :data-id="message.id"
    :data-read="message.date_read ? 'true' : 'false'"
    :class="[isIncoming ? 'message--incoming' : 'message--outcoming']"
  >
    <div class="message__wrapper">
      <div
        v-if="message.body"
        ref="content"
        class="message__content markdown-body"
        :class="[isIncoming && 'dark', isSingleLine && isFile && 'is-single-line']"
        v-html="message.body"
      />

      <div v-if="message.file" class="message__file" @click="handleFileClick">
        <div v-if="message.file.type === 2" class="message__file-image">
          <img :src="message.file.url" :alt="message.file.file_name" />
        </div>
        <div v-else class="message__file-icon">
          <UiSvgIcon name="file" />
        </div>
        <div class="message__file-meta">
          <div class="message__file-title">{{ message.file.file_name }}</div>
          <div class="message__file-size"></div>
        </div>
      </div>

      <div class="message__meta">
        <div class="message__time">{{ timestamp }}</div>
        <!-- <div v-if="message.date_read" class="message__seen">
          <UiSvgIcon name="checkmark" />
        </div> -->
      </div>
      <div class="message__more">
        <div class="message__more-trigger" @click="handleExpandedClick">
          <UiSvgIcon name="more-dots" />
        </div>
        <div class="message__more-actions" :class="[isMoreExpanded && 'is-active']">
          <a @click="handleReplyClick">Ответить</a>
          <a @click="handleCopyClick">Скопировать</a>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { mapGetters } from 'vuex';
import { timeToHHMM } from '~/helpers/Date';

export default {
  name: 'ChatMessages',
  props: {
    message: Object,
  },
  data() {
    return {
      isMoreExpanded: false,
      isSingleLine: false,
    };
  },
  computed: {
    isIncoming() {
      const isSupportMessage = this.message.user.is_support && this.user.is_support;

      if (this.user.is_support) {
        if (isSupportMessage) {
          return true;
        }
        return false;
      }

      return this.message.user.id === this.user.id;
    },
    isFile() {
      return this.message.file;
    },
    timestamp() {
      return timeToHHMM(this.message.date_created);
    },
    ...mapGetters('auth', ['user']),
  },
  mounted() {
    if (this.$refs.content) {
      this.$refs.content.querySelectorAll('code').forEach((block) => {
        window.hljs.highlightElement(block);
      });

      // if (/\r|\n/.exec(this.message.body)) {
      //   this.isSingleLine = false;
      // }

      this.isSingleLine = this.$refs.content.offsetHeight < 25;
    }
  },
  methods: {
    handleExpandedClick(e) {
      this.isMoreExpanded = !this.isMoreExpanded;
    },
    handleReplyClick() {},
    handleCopyClick() {
      const textArea = document.createElement('textarea');
      textArea.value = this.message.body;
      textArea.style.opacity = '0';
      document.body.appendChild(textArea);
      textArea.focus();
      textArea.select();

      try {
        const successful = document.execCommand('copy');
        if (successful) {
          this.$toast.global.default({ message: 'Сообщение успешно скопировано ' });
        } else {
          this.$toast.global.error({ message: 'Ошибка! Сообщение не скопировано ' });
        }
      } catch (err) {
        this.$toast.global.error({ message: `Ошибка! ${err.message}` });
      }

      document.body.removeChild(textArea);
    },
    handleFileClick() {
      // if (this)
    },
  },
};
</script>

<style lang="scss" scoped>
.message {
  margin: 8px 0;
  display: flex;
  &__wrapper {
    position: relative;
    padding: 14px 16px 7px;
    max-width: 440px;
    background: #fff;
    box-shadow: 0 6px 24px -4px rgba(23, 24, 24, 0.1);
    border-radius: 8px;
  }
  &__content {
    font-size: 15px;
    &.is-single-line {
      padding-right: 44px;
      // padding-right: 60px;
      margin-bottom: -14px;
    }
    ::v-deep code {
      border-radius: 8px;
    }
  }
  &__file {
    display: flex;
    align-items: center;
    padding-right: 44px;
    margin-top: -4px;
    margin-bottom: -18px;
    cursor: pointer;
    transition: opacity 0.25s $ease;
    &:hover {
      opacity: 0.8;
    }
  }
  &__file-image,
  &__file-icon {
    position: relative;
    z-index: 1;
    flex: 0 0 32px;
    width: 32px;
    height: 32px;
    overflow: hidden;
  }
  &__file-image {
    border-radius: 8px;
    img {
      position: absolute;
      left: 0;
      top: 0;
      width: 100%;
      height: 100%;
      object-fit: cover;
    }
  }
  &__file-icon {
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    color: white;

    .svg-icon {
      font-size: 16px;
    }
  }
  &__file-meta {
    padding-left: 8px;
  }
  &__file-title {
    font-size: 15px;
    line-height: 150%;
  }
  &__meta {
    margin-top: 2px;
    display: flex;
    align-items: center;
    justify-content: flex-end;
  }
  &__time {
    font-size: 13px;
    text-align: right;
    opacity: 0.5;
  }
  &__seen {
    font-size: 0;
    margin-left: 6px;
    opacity: 0.5;
    .svg-icon {
      font-size: 8px;
    }
  }
  &__more {
    position: absolute;
    right: 4px;
    top: 8px;
    opacity: 0;
    transition: opacity 0.25s $ease;
  }
  &__more-trigger {
    display: flex;
    align-items: center;
    justify-content: center;
    min-width: 20px;
    min-height: 20px;
    font-size: 13px;
    cursor: pointer;
  }
  &__more-actions {
    position: absolute;
    left: 0;
    top: 100%;
    z-index: 2;
    background: #fff;
    border-radius: 8px;
    padding: 8px;
    color: $fontColor;
    box-shadow: 0 6px 24px -4px rgba(23, 24, 24, 0.04);
    opacity: 0;
    will-change: opacity;
    transition: opacity 0.25s $ease;
    &.is-active {
      opacity: 1;
    }
    a {
      display: block;
      padding: 8px;
      font-size: 15px;
      cursor: pointer;
      transition: color 0.25s $ease;
      &:hover {
        color: $colorPrimary;
      }
    }
  }
  &:hover {
    .message {
      &__more {
        opacity: 1;
      }
    }
  }
  &--incoming {
    justify-content: flex-start;
    padding-right: 24px;
    .message__wrapper {
      background: $colorPrimary;
      color: white;
    }
  }
  &--outcoming {
    justify-content: flex-start;
    padding-right: 24px;
    .message__more-trigger {
      color: $colorPrimary;
    }
  }
}
</style>
