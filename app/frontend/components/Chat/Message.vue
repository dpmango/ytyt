<template>
  <div
    class="message"
    :data-id="message.id"
    :data-read="message.date_read ? 'true' : 'false'"
    :class="[isIncoming ? 'message--incoming' : 'message--outcoming']"
  >
    <div class="message__wrapper">
      <div ref="content" class="message__content markdown-body" :class="[isIncoming && 'dark']" v-html="message.body" />
      <div class="message__meta">
        <div class="message__time">{{ timestamp }}</div>
        <div v-if="message.date_read" class="message__seen">
          <UiSvgIcon name="checkmark" />
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { mapGetters } from 'vuex';
import { timeToTimeStamp } from '~/helpers/Date';

export default {
  name: 'ChatMessages',
  props: {
    message: Object,
  },
  computed: {
    isIncoming() {
      return this.message.user.id === this.user.id;
    },
    timestamp() {
      return timeToTimeStamp(this.message.date_created);
    },
    ...mapGetters('auth', ['user']),
  },
  mounted() {
    if (this.$refs.content) {
      this.$refs.content.querySelectorAll('code').forEach((block) => {
        window.hljs.highlightElement(block);
      });
    }
  },
};
</script>

<style lang="scss" scoped>
.message {
  margin: 4px 0;
  display: flex;
  &__wrapper {
    position: relative;
    padding: 14px 16px;
    max-width: 600px;
    background: #fff;
    box-shadow: 0 6px 24px -4px rgba(23, 24, 24, 0.1);
    border-radius: 8px;
  }
  &__content {
    font-size: 15px;
    ::v-deep code {
      border-radius: 8px;
    }
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
  &--incoming {
    justify-content: flex-end;
    padding-left: 24px;
    .message__wrapper {
      background: #1e88e5;
      color: white;
    }
  }
  &--outcoming {
    justify-content: flex-start;
    padding-right: 24px;
  }
}
</style>
