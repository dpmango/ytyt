<template>
  <div class="dialogs">
    <div class="dialogs__list">
      <div v-for="dialog in dialogs" :key="dialog.id" class="dialog">
        <div class="dialog__avatar">
          <div class="dialog__avatar-image">
            <img :src="dialog.avatar" :alt="dialog.name" />
          </div>
        </div>
        <div class="dialog__content">
          <div class="dialog__title">
            <span class="dialog__title-name">{{ dialog.name }}</span>
            <div class="dialog__indicator">
              <span>{{ dialog.indicator }}</span>
            </div>
            <div class="dialog__time">{{ dialog.time }}</div>
          </div>
          <div class="dialog__description">{{ dialog.description }}</div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  props: {
    dialogs: Array,
  },
};
</script>

<style lang="scss" scoped>
.dialogs {
  flex: 0 0 auto;
  display: flex;
  flex-direction: column;
  overflow-y: auto;
  &__list {
    flex: 1 0 auto;
  }
}

.dialog {
  display: flex;
  border-bottom: 1px solid rgba(147, 149, 152, 0.2);
  border-right: 1px solid rgba(147, 149, 152, 0.2);
  padding: 19px 12px;
  transition: background 0.25s $ease;
  cursor: pointer;
  &:last-child {
    border-bottom: 0;
  }
  &:hover {
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
