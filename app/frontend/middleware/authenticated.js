export default function ({ store, redirect }) {
  // redirect authenticated users for some pages
  // like login, signup (no need) and homepage landing (by design)

  if (store.getters['auth/isAuthenticated']) {
    return redirect('/course');
  }
}
