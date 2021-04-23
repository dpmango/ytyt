<template>
  <div class="dialogs">
    <div class="dialogs__list">
      <ChatDialog
        v-for="dialog in dialogs"
        :key="dialog.id"
        :dialog="dialog"
        :active-dialog="activeDialog"
        @setDialog="setDialog(dialog.id)"
      />
    </div>
  </div>
</template>

<script>
export default {
  props: {
    dialogs: Array,
    activeDialog: Number,
    setDialog: Function,
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
</style>
