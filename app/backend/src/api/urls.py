from django.urls import include, path, re_path
from rest_framework import routers
from rest_framework_jwt.views import refresh_jwt_token

from constants.api.views import ConstantsViewSet
from courses.api.course.views import CourseViewSet
from courses.api.course_lesson.views import CourseLessonViewSet
from courses.api.course_theme.views import CourseThemeViewSet
from courses.api.lesson_fragment.views import LessonFragmentViewSet
from files.api.views import FileUploadView
from payment.api.views import PaymentViewSet
from search.api.views import SearchViewSet
from users.api.auth.logout import LogoutViewCustom
from users.api.auth.views import (
    PasswordResetView,
    UserDetailsView,
    PasswordResetConfirmViewCustom,
    PasswordChangeViewCustom,
    LoginViewCustom,
)
from users.api.feedback.views import feedback
from users.api.registration.views import RegisterView, VerifyEmailView

router = routers.DefaultRouter()
router.register(r'files', FileUploadView, basename='files')
router.register(r'payment', PaymentViewSet, basename='payment')
router.register(r'constants', ConstantsViewSet, basename='constants')
router.register(r'search', SearchViewSet, basename='search')
router.register(r'courses', CourseViewSet, basename='courses')
router.register(r'courses/(?P<course_id>\d+)/themes', CourseThemeViewSet, basename='courses-themes')
router.register(r'courses/(?P<course_id>\d+)/themes/(?P<course_theme_id>\d+)/lessons', CourseLessonViewSet,
                basename='courses-lessons')
router.register(r'lessons-fragments', LessonFragmentViewSet, basename='lessons-fragments')


urlpatterns = [
    re_path('^api/feedback/', feedback, name='feedback'),
    path('api/', include(router.urls)),

    re_path(r'^rest-auth/token-refresh/$', refresh_jwt_token),
    re_path(r'^rest-auth/password/reset/confirm$', PasswordResetConfirmViewCustom.as_view()),
    re_path(r'^rest-auth/password/reset/$', PasswordResetView.as_view()),
    re_path(r'^rest-auth/password/change/$', PasswordChangeViewCustom.as_view()),
    re_path(r'^rest-auth/logout/$', LogoutViewCustom.as_view()),
    re_path(r'^rest-auth/login/$', LoginViewCustom.as_view()),
    re_path(r'^rest-auth/user/$', UserDetailsView.as_view(), name='rest_user_details'),

    re_path(r'^rest-auth/registration/verify/', VerifyEmailView.as_view(), name='rest_verify_email'),
    re_path(r'^rest-auth/registration/', RegisterView.as_view(), name='rest_register'),
]
