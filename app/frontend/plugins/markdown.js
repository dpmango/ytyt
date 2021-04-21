import Vue from 'vue';
import VueSimplemde from 'vue-simplemde';
import hljs from 'highlight.js';
import SimpleMDE from 'simplemde';

Vue.component('VueSimplemde', VueSimplemde);

export default function ({ $config }, inject) {
  inject('SimpleMDE', SimpleMDE);
}

window.hljs = hljs;
