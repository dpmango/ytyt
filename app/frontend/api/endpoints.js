const auth = '/rest-auth';
const api = '/api';

export default {
  auth: {
    user: `${auth}/user/`,
    login: `${auth}/login/`,
    logout: `${auth}/logout/`,
    registration: `${auth}/registration/`,
    verifyEmail: `${auth}/registration/verify/`,
    refreshToken: `${auth}/token-refresh/`,
    passwordChange: `${auth}/password/change/`,
    passwordReset: `${auth}/password/reset/`,
    passwordResetConfirm: `${auth}/password/reset/confirm/`,
  },
  course: {
    courses: `${api}/courses/`,
    themes: `${api}/courses/:id/themes/`,
    lessons: `${api}/courses/:course_id/themes/:theme_id/lessons/`,
    lesson: `${api}/courses/:course_id/themes/:theme_id/lessons/:fragment_id/`,
    complete: `${api}/lessons-fragments/:id/completed/`,
    search: `${api}/search/`,
  },
  chat: {
    files: `${api}/files/`,
  },
  constants: {
    get: `${api}/constants/`,
  },
  payment: {
    init: `${api}/payment/init/`,
    initInstallment: `${api}/payment/init-installment/`,
  },
  feedback: {
    base: `${api}/feedback/`,
  },
};
