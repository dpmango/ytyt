import Vue from 'vue';
import VueFinalModal from 'vue-final-modal/lib';

Vue.use(VueFinalModal());

export default function ({ ...context }, inject) {
  // Inject to context as $api
  inject('modal', VueFinalModal);
}
