export default function ({ store, redirect }) {
  store.dispatch('auth/checkToken');

  // if (store.getters['auth/isAuthenticated']) {
  //   return redirect('/course');
  // }
}
