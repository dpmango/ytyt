<template>
  <div
    class="dialog"
    :data-id="dialog.id"
    :class="[activeDialog === dialog.id && 'is-current']"
    @click="$emit('setDialog', dialog.id)"
  >
    <div class="dialog__avatar">
      <div class="dialog__avatar-image">
        <img :src="user.thumbnail_avatar" :alt="user.first_name" />
      </div>
    </div>
    <div class="dialog__content">
      <div class="dialog__title">
        <span class="dialog__title-name">{{ title }}</span>
        <div v-if="dialog.unread_messages_count" class="dialog__indicator">
          <span>{{ dialog.unread_messages_count }}</span>
        </div>
        <div class="dialog__time">{{ timestamp }}</div>
      </div>
      <div class="dialog__description" v-html="message.body" />
    </div>
  </div>
</template>

<script>
import { timeToTimeStamp } from '~/helpers/Date';

export default {
  props: {
    dialog: Object,
    activeDialog: Number,
  },
  computed: {
    message() {
      return this.dialog.last_message;
    },
    user() {
      return this.dialog.user;
    },
    title() {
      const { first_name, last_name, email } = this.user;

      if (first_name) {
        return `${first_name} ${last_name}`;
      } else {
        return email;
      }
    },
    timestamp() {
      return timeToTimeStamp(this.message.date_created);
    },
  },
};
</script>

<style lang="scss" scoped>
.dialog {
  display: flex;
  border-bottom: 1px solid rgba(147, 149, 152, 0.2);
  padding: 17px 12px;
  transition: background 0.25s $ease;
  cursor: pointer;
  &:last-child {
    border-bottom: 0;
  }
  &:hover {
    background: rgba(155, 81, 224, 0.06);
  }
  &.is-current {
    background: rgba(155, 81, 224, 0.06);
  }
  &__avatar {
    flex: 0 0 40px;
    max-width: 40px;
  }
  &__avatar-image {
    position: relative;
    z-index: 1;
    width: 40px;
    height: 40px;
    border-radius: 50%;
    background: $colorGray;
    overflow: hidden;
    img {
      position: absolute;
      top: 0;
      left: 0;
      width: 100%;
      height: 100%;
      object-fit: contain;
    }
  }

  &__content {
    flex: 0 0 calc(100% - 40px);
    max-width: calc(100% - 40px);
    min-width: 1px;
    padding-left: 12px;
  }
  &__title {
    position: relative;
    display: flex;
    align-items: center;
  }
  &__title-name {
    font-weight: 500;
    font-size: 15px;
    margin-right: 6px;
    @include text-overflow;
  }
  &__indicator {
    width: 20px;
    height: 20px;
    display: flex;
    align-items: center;
    justify-content: center;
    text-align: center;
    border-radius: 50%;
    background: $colorRed;
    color: white;
    span {
      font-size: 12px;
    }
  }
  &__time {
    flex: 0 0 auto;
    margin-left: auto;
    padding-left: 10px;
    font-size: 12px;
    text-align: right;
    color: rgba(#171818, 0.5);
  }
  &__description {
    display: flex;
    font-size: 14px;
    color: rgba($fontColor, 0.7);
    @include text-overflow;
    ::v-deep * {
      margin: 0 6px 0 0;
      @include text-overflow;
    }
  }
}
</style>
