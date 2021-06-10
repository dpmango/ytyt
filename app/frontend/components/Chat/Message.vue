<template>
  <div
    class="message"
    :data-id="message.id"
    :data-read="message.date_read ? 'true' : 'false'"
    :class="[isIncoming ? 'message--incoming' : 'message--outcoming', message.isGhost && 'is-ghost']"
  >
    <div class="message__wrapper" :class="[isFile && 'is-file']">
      <NuxtLink
        v-if="message.lesson"
        :to="`/theme/${message.lesson.course_theme_id}/${message.lesson.id}`"
        class="message__lesson"
      >
        <span>{{ message.lesson.title }}</span>
      </NuxtLink>

      <div
        v-if="message.body"
        ref="content"
        class="message__content markdown-body"
        :class="[isIncoming && 'dark', (isSingleLine || isFile) && 'is-single-line']"
        v-html="messageBody"
      />

      <div v-if="message.file" class="message__file" @click="handleFileClick">
        <div v-if="message.file.type === 2" v-viewer class="message__file-image">
          <img :src="fileImageUrl" :alt="message.file.file_name" />
        </div>
        <div v-else class="message__file-icon">
          <UiSvgIcon name="file" />
        </div>
        <div class="message__file-meta">
          <div class="message__file-title">{{ message.file.file_name }}</div>
          <div class="message__file-size">{{ fileSize }}</div>
        </div>
      </div>

      <div class="message__meta">
        <div class="message__time">{{ timestamp }}</div>
        <!-- <div v-if="message.date_read" class="message__seen">
          <UiSvgIcon name="checkmark" />
        </div> -->
      </div>
      <div class="message__more">
        <div class="message__more-trigger">
          <UiSvgIcon name="more-dots" />
        </div>
        <div class="message__more-wrapper">
          <div class="message__more-actions">
            <a @click="handleReplyClick">Ответить</a>
            <a @click="handleCopyClick">Скопировать</a>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { mapMutations, mapGetters } from 'vuex';
import { timeToHHMM } from '~/helpers/Date';
import { formatBytes } from '~/helpers/FormatBytes';

export default {
  name: 'ChatMessages',

  props: {
    message: Object,
  },
  data() {
    return {
      isSingleLine: false,
    };
  },
  computed: {
    messageBody() {
      return this.message.body;
    },
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
    fileImageUrl() {
      if (this.message.file.thumb) {
        return this.message.file.thumb.size_100x100;
      }
      return this.message.file.url;
    },
    fileSize() {
      return formatBytes(this.message.file.size);
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
    handleReplyClick() {
      this.setReplyId(this.message.id);
    },
    handleCopyClick() {
      const textArea = document.createElement('textarea');
      textArea.value = this.message.markdown_body;
      textArea.style.opacity = '0';
      document.body.appendChild(textArea);
      textArea.focus();
      textArea.select();

      try {
        const successful = document.execCommand('copy');
        if (!successful) {
          this.$toast.global.error({ message: 'Ошибка! Сообщение не скопировано ' });
        }
      } catch (err) {
        this.$toast.global.error({ message: `Ошибка! ${err.message}` });
      }

      document.body.removeChild(textArea);
    },
    handleFileClick() {
      if (this.message.file.type !== 2) {
        window.open(this.message.file.url);
      } else {
        this.$viewerApi({
          options: {
            navbar: false,
            toolbar: false,
            movable: false,
            rotatable: false,
            zoomOnWheel: false,
          },
          images: [this.message.file.url],
        });
      }
    },
    ...mapMutations('chat', ['setReplyId']),
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
    &:hover {
      .message {
        &__more {
          opacity: 1;
        }
      }
    }
    &.is-file {
      .message__more {
        display: none;
      }
    }
  }
  &__lesson {
    display: inline-block;
    font-size: 14px;
    margin-bottom: 5px;
    opacity: 0.6;
    transition: opacity 0.25s $ease;
    span {
      position: relative;
      display: inline-block;
      padding-bottom: 4px;
      &::after {
        display: inline-block;
        content: '';
        position: absolute;
        bottom: 0;
        left: 0;
        right: 0;
        border-bottom: 1px dashed currentColor;
      }
    }
    &:hover {
      opacity: 1;
    }
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
    ::v-deep pre code {
      border-radius: 0;
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
    background: $colorPrimary;
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
    line-height: 1.2;
  }
  &__file-size {
    margin-top: 2px;
    font-size: 13px;
    line-height: 1.2;
    opacity: 0.5;
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
    z-index: 2;
    right: 4px;
    top: 8px;
    opacity: 0;
    will-change: opacity;
    backface-visibility: hidden;
    transition: opacity 0.25s $ease;
    &:hover {
      .message__more-wrapper {
        // opacity: 1;
        display: block;
      }
    }
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
  &__more-wrapper {
    position: absolute;
    left: -20px;
    top: 100%;
    padding-top: 10px;
    min-width: 160px;
    display: none;
  }
  &__more-actions {
    position: relative;
    background: #fff;
    border-radius: 8px;
    padding: 8px;
    color: $fontColor;
    box-shadow: 0 6px 24px -4px rgba(23, 24, 24, 0.04);
    &::before {
      display: inline-block;
      content: '';
      position: absolute;
      top: -7px;
      left: 19px;
      background: url('~assets/landing/img/help-polygon.svg') no-repeat 50% 50%;
      width: 22px;
      height: 14px;
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
  &--incoming {
    justify-content: flex-start;
    padding-right: 24px;
    .message__wrapper {
      background: $colorPrimary;
      color: white;
    }
    .message__file-icon {
      background: white;
      color: $colorPrimary;
    }
  }
  &--outcoming {
    justify-content: flex-start;
    padding-right: 24px;
    .message__more-trigger {
      color: $colorPrimary;
    }
  }
  &.is-ghost {
    opacity: 0.5;
    pointer-events: none;
  }
}

.messages__group:last-child .message:last-child {
  .message {
    &__more-wrapper {
      top: auto;
      bottom: 100%;
      padding-top: 0;
      padding-bottom: 10px;
    }
    &__more-actions {
      &::before {
        top: auto;
        bottom: -10px;
        transform: rotate(180deg);
      }
    }
  }
}

.chat.is-mini {
  .message {
    &__more-wrapper {
      right: -20px;
      left: auto;
      min-width: 1px;
    }
    &__more-actions {
      &::before {
        left: auto;
        right: 19px;
      }
    }
  }
}
</style>
