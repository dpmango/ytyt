<template>
  <div class="dialog" :class="[activeDialog === dialog.id && 'is-current']" @click="$emit('setDialog', dialog.id)">
    <div class="dialog__avatar">
      <div class="dialog__avatar-image">
        <img :src="user.thumbnail_avatar" :alt="user.first_name" />
      </div>
    </div>
    <div class="dialog__content">
      <div class="dialog__title">
        <span class="dialog__title-name"> {{ user.first_name }} {{ user.last_name }} </span>
        <!-- <div class="dialog__indicator">
          <span>{{ dialog.indicator }}</span>
        </div> -->
        <div class="dialog__time">{{ timestamp }}</div>
      </div>
      <div class="dialog__description">{{ message.body }}</div>
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
      return this.dialog.last_message.user;
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
    font-size: 14px;
    color: rgba($fontColor, 0.7);
    @include text-overflow;
  }
}
</style>
