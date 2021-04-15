from django.urls import include, path, re_path
from rest_framework import routers

from constants.api.views import ConstantsViewSet
from courses.api.course.views import CourseViewSet
from courses.api.course_lesson.views import CourseLessonViewSet
from courses.api.course_theme.views import CourseThemeViewSet
from courses.api.lesson_fragment.views import LessonFragmentViewSet
from search.api.views import SearchViewSet
from users.api.auth.views import PasswordResetView
from users.api.registration.views import RegisterView, VerifyEmailView

router = routers.DefaultRouter()
router.register(r'constants', ConstantsViewSet, basename='constants')
router.register(r'search', SearchViewSet, basename='search')
router.register(r'courses', CourseViewSet, basename='courses')
router.register(r'courses/(?P<course_id>\d+)/themes', CourseThemeViewSet, basename='courses-themes')
router.register(r'courses/(?P<course_id>\d+)/themes/(?P<course_theme_id>\d+)/lessons', CourseLessonViewSet,
                basename='courses-lessons')
router.register(r'lessons-fragments', LessonFragmentViewSet, basename='lessons-fragments')


urlpatterns = [
    path('api/', include(router.urls)),

    re_path(r'^rest-auth/password/reset/$', PasswordResetView.as_view()),
    re_path(r'^rest-auth/', include('rest_auth.urls')),

    re_path(r'^rest-auth/registration/verify-email/', VerifyEmailView.as_view(), name='rest_verify_email'),
    re_path(r'^rest-auth/registration/', RegisterView.as_view(), name='rest_register'),
]
