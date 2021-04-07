import Vue from 'vue';

Vue.filter('uppercase', (val) => val.toUpperCase());
Vue.filter('lovercase', (val) => val.toLoverCase());
Vue.filter('integer', (val) => parseInt(val));
Vue.filter('capitalize', (val) => {
  if (!val) {
    return '';
  }
  val = val.toString();
  return val.charAt(0).toUpperCase() + val.slice(1);
});
