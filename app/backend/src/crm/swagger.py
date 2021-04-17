from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions


schema_view = get_schema_view(
    openapi.Info(
        title="Course Platform",
        default_version='v1',
        description="Course Platform API",
        contact=openapi.Contact(
            name='Konyaev Matvey',
            email='mat.coniaev2012@yandex.ru'
        )
    ),
    public=True,
    permission_classes=(permissions.IsAdminUser,),
)
