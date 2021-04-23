<template>
  <vue-simplemde
    ref="markdownEditor"
    v-model="value"
    :highlight="true"
    :configs="config"
    preview-class="markdown-body"
  />
</template>

<script>
import { mapActions, mapGetters } from 'vuex';

export default {
  data() {
    return {
      value: '',
      config: {
        spellChecker: false,
        status: false,
        toolbar: [
          {
            name: 'image',
            action: this.$SimpleMDE.drawImage,
            className: 'fa fa-picture-o',
            title: 'Insert Image',
          },
        ],
      },
    };
  },
  computed: {},
  watch: {
    value(newVal, oldVal) {
      this.$emit('change', newVal);
    },
  },
};
</script>

<style lang="scss">
@import 'simplemde/dist/simplemde.min.css';
@import 'github-markdown-css';
@import 'highlight.js/styles/atom-one-dark.css';
</style>

<style lang="scss">
.CodeMirror,
.CodeMirror-scroll {
  min-height: 100px;
  max-height: 300px;
}

.CodeMirror {
  padding: 16px;
  border: 0;
  border-top: 1px solid rgba(147, 149, 152, 0.2);
}

.CodeMirror-scroll {
  margin-bottom: -32px;
  padding-bottom: 32px;
}

.vue-simplemde {
  .markdown-body {
    padding: 16px !important;
  }
  .editor-toolbar {
    border-top: 0;
    border-left: 0;
    border-right: 0;
  }
}
</style>
