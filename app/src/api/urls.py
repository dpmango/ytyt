from django.urls import include, path, re_path
from rest_framework import routers

from courses.api.views import CoursesViewSet

router = routers.DefaultRouter()
router.register(r'courses', CoursesViewSet, basename='users')


# Wire up our API using automatic URL routing.
urlpatterns = [
    path('api/', include(router.urls)),
    re_path(r'^rest-auth/', include('rest_auth.urls')),
    re_path(r'^rest-auth/registration/', include('rest_auth.registration.urls')),
]
