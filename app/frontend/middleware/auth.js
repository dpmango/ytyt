// import Cookies from 'js-cookie';

export default function ({ store, redirect }) {
  // Check if user is not authenticated
  // const token = process.client ? Cookies.get('ytyt_token') : 0;

  store.dispatch('auth/checkToken');

  if (!store.getters['auth/isAuthenticated']) {
    return redirect('/auth/login');
  }
}
