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
          <textarea :id="`editor__${id}`" v-model="value" class="editor__block brython__editor-main"></textarea>
          <div class="brython__console">
            <textarea :id="`console__${id}`" ref="textarea" class="console__stdout" autocomplete="off"></textarea>
          </div>
        </div>
      </div>
    </div>
  </client-only>
</template>

<script>
import uniqueId from 'lodash/uniqueId';

export default {
  props: {
    ready: Boolean,
    code: String,
  },
  data() {
    return {
      value: this.code,
    };
  },
  computed: {
    id() {
      return uniqueId();
    },
  },
  // mounted() {
  //   console.log('brython snippet mounted - id', this.id, this.ready);
  // },
  watch: {
    ready(newVal, oldVal) {
      if (newVal === true) {
        if (this.$refs.textarea) {
          this.$refs.textarea.addEventListener('stdout_result', this.handleTextareaChange, false);
          this.$refs.textarea.addEventListener('keydown', this.handleTextareaKeydown, false);
        }
      }
    },
  },

  beforeDestroy() {
    if (this.$refs.textarea) {
      this.$refs.textarea.removeEventListener('stdout_result', this.handleTextareaChange, false);
      this.$refs.textarea.removeEventListener('keydown', this.handleTextareaKeydown, false);
    }
  },
  methods: {
    handleTextareaChange(e) {
      console.log('stdout_result event', e);

      let rows = e.stdout_rows || 1;

      if (e.stdout_result) {
        const temp_stdout = document.createElement('div');
        temp_stdout.innerHTML = e.stdout_result;
        temp_stdout.classList.add('brython__stdout');
        document.querySelector('.lesson__box').appendChild(temp_stdout);

        rows = Math.ceil(temp_stdout.offsetHeight / 20);
        if (rows <= 0) rows = 1;
        if (rows >= 7) rows = 7;

        temp_stdout.remove();
      }

      e.target.setAttribute('rows', rows);
    },
    handleTextareaKeydown(e) {
      if ((e.ctrlKey || e.shiftKey) && e.keyCode === 13) {
        e.preventDefault();

        document.querySelector(`#run__${this.id}`).dispatchEvent(new Event('click'));
      }
    },
  },
};
</script>

<style lang="scss">
.brython__stdout {
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  padding: 8px 36px;
  font-size: 15px;
  opacity: 0.01;
}
</style>

<style lang="scss" scoped>
.brython {
  position: relative;
  margin: 1em 0;
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
