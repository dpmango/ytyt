export default {
  auth: {
    user: '/rest-auth/user/',
    login: '/rest-auth/login/',
    logout: '/rest-auth/logout/',
    passwordChange: '/rest-auth/password/change/',
    passwordReset: '/rest-auth/password/reset/',
    passwordResetConfirm: '/rest-auth/password/reset/confirm/',
    registration: '/rest-auth/registration/',
    verifyEmail: '/rest-auth/registration/verify-email/',
  },
  course: {
    courses: '/api/courses/',
    themes: '/api/courses/:id/themes/',
    lessons: '/api/courses/:course_id/themes/:theme_id/lessons/',
    lesson: '/api/courses/:course_id/themes/:theme_id/lessons/:fragment_id/',
    complete: '/api/lessons-fragments/:id/completed/',
    search: '/api/search/',
  },
};
