<template>
  <client-only>
    <div class="brython">
      <iframe ref="iframe" src="/brython/example.html" onload="window.resizeIframe(this)" />
    </div>
  </client-only>
</template>

<script>
export default {
  head() {
    return {
      script: [
        // {
        //   src: '/brython/brython.js',
        // },
        // {
        //   src: '/brython/brython_stdlib.js',
        // },
        // {
        //   src: '/brython/ace/ace.js',
        // },
        // {
        //   src: '/brython/ace/ext-language_tools.js',
        // },
      ],
    };
  },
  mounted() {
    setTimeout(() => {
      this.$refs.iframe.contentWindow.document.addEventListener('view.updated', () => {
        window.resizeIframe(this.$refs.iframe);
      });
    }, 500);

    window.resizeIframe = (obj) => {
      obj.style.height = obj.contentWindow.document.documentElement.scrollHeight + 'px';
    };
  },
};
</script>

<style lang="scss" scoped>
.brython {
  position: relative;
  iframe {
    width: 100%;
    max-height: 600px;
    height: auto;
    border: 0;
    box-shadow: none;
  }
}
</style>
