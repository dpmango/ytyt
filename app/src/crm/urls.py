from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from crm.swagger import schema_view


urlpatterns = [
    path('markdownx/', include('markdownx.urls')),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('admin/', admin.site.urls),
    path('', include('api.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
