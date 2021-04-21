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
            name: 'bold',
            action: this.$SimpleMDE.toggleBold,
            className: 'fa fa-bold',
            title: 'Bold',
          },
          {
            name: 'italic',
            action: this.$SimpleMDE.toggleItalic,
            className: 'fa fa-italic',
            title: 'Italic',
          },
          {
            name: 'heading',
            action: this.$SimpleMDE.toggleHeadingSmaller,
            className: 'fa fa-header',
            title: 'Heading',
          },
          '|',
          {
            name: 'Quote',
            action: this.$SimpleMDE.toggleBlockquote,
            className: 'fa fa-quote-left',
            title: 'Quote',
          },
          {
            name: 'unordered-list',
            action: this.$SimpleMDE.toggleUnorderedList,
            className: 'fa fa-list-ul',
            title: 'Generic List',
          },
          {
            name: 'ordered-list',
            action: this.$SimpleMDE.toggleOrderedList,
            className: 'fa fa-list-ol',
            title: 'Generic List',
          },
          '|',
          {
            name: 'code',
            action: this.$SimpleMDE.toggleCodeBlock,
            className: 'fa fa-code',
            title: 'Code',
          },
          {
            name: 'link',
            action: this.$SimpleMDE.drawLink,
            className: 'fa fa-link',
            title: 'Create Link',
          },
          {
            name: 'image',
            action: this.$SimpleMDE.drawImage,
            className: 'fa fa-picture-o',
            title: 'Insert Image',
          },
          // {
          //   name: 'custom',
          //   className: 'fa fa-star',
          //   title: 'Custom Button',
          // },
          '|',
          {
            name: 'preview',
            action: this.$SimpleMDE.togglePreview,
            className: 'fa fa-eye no-disable',
            title: 'Toggle Preview',
          },
          '|',
          {
            name: 'guide',
            action(editor) {
              window.open('https://simplemde.com/markdown-guide');
            },
            className: 'fa fa-question-circle',
            title: 'Markdown Guide',
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
