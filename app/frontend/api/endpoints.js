export default {
  auth: {
    user: '/rest-auth/user/',
    login: '/rest-auth/login/',
    logout: '/rest-auth/logout/',
    registration: '/rest-auth/registration/',
    refreshToken: '/rest-auth/token-refresh/',
    verifyEmail: '/rest-auth/registration/verify-email/',
    passwordChange: '/rest-auth/password/change/',
    passwordReset: '/rest-auth/password/reset/',
    passwordResetConfirm: '/rest-auth/password/reset/confirm/',
  },
  course: {
    courses: '/api/courses/',
    themes: '/api/courses/:id/themes/',
    lessons: '/api/courses/:course_id/themes/:theme_id/lessons/',
    lesson: '/api/courses/:course_id/themes/:theme_id/lessons/:fragment_id/',
    complete: '/api/lessons-fragments/:id/completed/',
    search: '/api/search/',
  },
  chat: {
    files: '/api/files/',
  },
};
