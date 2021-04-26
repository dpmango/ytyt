<template>
  <div class="dialogs">
    <ChatDialog
      v-for="dialog in dialogs"
      :key="dialog.id"
      :dialog="dialog"
      :active-dialog="activeDialog"
      @setDialog="setDialog(dialog.id)"
    />
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
  flex: 1 0 auto;
}
</style>
