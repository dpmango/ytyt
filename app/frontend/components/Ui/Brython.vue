<template>
  <client-only>
    <div class="brython" :class="[!ready && 'is-loading']">
      <template v-if="!ready">
        <UiLoader :loading="true" theme="block" />
      </template>

      <div :id="`container__${id}`" class="brython__editor">
        <div class="brython__actions">
          <button :id="`run__${id}`" class="run_stdin brython__run">
            <UiSvgIcon name="run-code" />
            <span>Запустить</span>
          </button>
        </div>

        <div class="brython__main">
          <textarea :id="`editor__${id}`" class="editor__block brython__editor-main">print('WOW!')</textarea>
          <div class="brython__console">
            <textarea :id="`console__${id}`" class="console__stdout" readonly autocomplete="off"></textarea>
          </div>
        </div>
      </div>

      <!-- <script type="text/python3">
        from browser import document as doc, window
        from editor import EditorCodeBlocks

        EditorCodeBlocks(doc, window).declare()
      </script> -->
    </div>
  </client-only>
</template>

<script>
export default {
  props: {
    ready: Boolean,
    id: String,
  },
};
</script>

<style lang="scss" scoped>
.brython {
  position: relative;
  margin: 1em 20px;
  .loader {
    position: absolute;
    background: rgba(white, 0.5);
    align-items: center;
    top: 0;
    right: 0;
    left: 0;
    bottom: 0;
    z-index: 5;
    margin: 0 !important;
  }
  &__editor {
    position: relative;
    height: 100%;
    max-height: 600px;
    display: flex;
    flex-direction: column;
  }

  &__actions {
    flex: 0 0 auto;
    display: block;
  }

  &__main {
    flex: 1 1 auto;
    min-height: 1px;
    display: flex;
    flex-direction: column;
  }

  &__editor-main {
    flex: 0 0 auto;
    width: 100%;
    border: 0;
  }

  &__console {
    position: relative;
    z-index: 2;
    flex: 1 1 auto;
    height: 100%;
    min-height: 1px;
    font-size: 0;
    overflow-y: auto;
    &::-webkit-scrollbar {
      width: 7px;
    }
    &::-webkit-scrollbar-track {
      border-radius: 0;
      background: #0a090c;
      box-shadow: inset 0 0 6px rgba(0, 0, 0, 0.3);
    }
    &::-webkit-scrollbar-thumb {
      background: #939598;
      border-radius: 4px;
    }
    textarea {
      -webkit-appearance: none;
      width: 100%;
      height: auto;
      margin: 0;
      padding: 8px 16px;
      font-size: 15px;
      border: 0;
      float: none;
      background-color: transparent;
      box-shadow: none;
      color: $fontColor;
      border-radius: 0;
      resize: none;
      &:focus,
      &:active {
        outline: none;
      }
    }
  }

  &__run {
    border: 0;
    display: flex;
    align-items: center;
    cursor: pointer;
    padding: 8px 16px;
    background: #38bff2;
    border-radius: 6px 6px 0 0;
    color: white;
    transition: background 0.25s $ease;
    .svg-icon {
      font-size: 24px;
    }
    span {
      display: inline-block;
      margin-left: 10px;
    }
    &:hover {
      background: $colorPrimaryHover;
    }
  }
  &.is-loading {
    .brython__editor-main {
      color: white;
    }
  }
}
</style>
