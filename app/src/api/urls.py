from django.urls import include, path, re_path
from rest_framework import routers

from courses.api.course.views import CourseViewSet
from courses.api.course_theme.views import CourseThemeViewSet
from courses.api.course_lesson.views import CourseLessonViewSet


router = routers.DefaultRouter()
router.register(r'courses', CourseViewSet, basename='courses')
router.register(r'courses/(?P<course_id>\d+)/themes', CourseThemeViewSet, basename='courses-theme')
router.register(r'courses/(?P<course_id>\d+)/themes/(?P<course_theme_id>\d+)/lessons',
                CourseLessonViewSet,
                basename='courses-lesson')


# Wire up our API using automatic URL routing.
urlpatterns = [
    path('api/', include(router.urls)),
    re_path(r'^rest-auth/', include('rest_auth.urls')),
    re_path(r'^rest-auth/registration/', include('rest_auth.registration.urls')),
]
