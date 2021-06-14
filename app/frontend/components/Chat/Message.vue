<template>
  <div
    class="message"
    :data-id="message.id"
    :data-read="message.date_read ? 'true' : 'false'"
    :data-support="message.user.is_support ? 'true' : 'false'"
    :class="[isIncoming ? 'message--incoming' : 'message--outcoming', message.isGhost && 'is-ghost']"
  >
    <div class="message__wrapper" :class="[isFile && 'is-file']">
      is_support {{ message.user.is_support }}
      <NuxtLink
        v-if="message.lesson"
        :to="`/theme/${message.lesson.course_theme_id}/${message.lesson.id}`"
        class="message__lesson"
      >
        <span>{{ message.lesson.title }}</span>
      </NuxtLink>
      <div v-if="message.reply" class="message__reply-body">
        <span>{{ message.reply.markdown_body }}</span>
      </div>

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
    </div>
    <div class="message__reply" @click="handleReplyClick">
      <UiSvgIcon name="reply" />
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

      this.isSingleLine = this.$refs.content.offsetHeight < 25;
    }
  },
  methods: {
    handleReplyClick() {
      this.setReply({
        id: this.message.id,
        text: this.message.markdown_body,
      });
    },
    handleFileClick() {
      if (this.message.file.type !== 2) {
        window.open(this.message.file.url);
      } else {
        window.$viewer = this.$viewerApi({
          options: {
            navbar: false,
            toolbar: false,
            movable: false,
            rotatable: false,
            zoomOnWheel: false,
            title: false,
            button: false,
            zoomable: false,
          },
          images: [this.message.file.url],
        });
      }
    },
    ...mapMutations('chat', ['setReply']),
  },
};
</script>

<style lang="scss" scoped>
.message {
  margin: 8px 0;
  display: flex;
  align-items: center;
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
      max-width: 100%;
      min-width: 1px;
      overflow: hidden;
      text-overflow: ellipsis;
      white-space: nowrap;
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
  &__reply-body {
    position: relative;
    display: block;
    max-width: 100%;
    min-width: 1px;
    font-size: 13px;
    margin-bottom: 5px;
    padding-left: 10px;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
    &::before {
      display: inline-block;
      content: '';
      position: absolute;
      bottom: 0;
      left: 0;
      top: 0;
      height: 20px;
      width: 2px;
      background: $colorPrimary;
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
    pointer-events: none;
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
  &__reply {
    flex: 0 0 auto;
    padding: 5px;
    margin-left: 7px;
    color: rgba($colorPrimary, 0.5);
    cursor: pointer;
    opacity: 0;
    transition: color 0.25s $ease, opacity 0.25s $ease;
    .svg-icon {
      font-size: 14px;
    }
    &:hover {
      color: $colorPrimary;
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
    .message__reply-body::before {
      background-color: white;
    }
  }
  &--outcoming {
    justify-content: flex-start;
    padding-right: 24px;
  }
  &.is-ghost {
    opacity: 0.5;
    pointer-events: none;
  }
  &:hover {
    .message__reply {
      opacity: 1;
    }
  }
}
</style>
