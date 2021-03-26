from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from crm.swagger import schema_view


urlpatterns = [
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('markdownx/', include('markdownx.urls')),
    path('martor/', include('martor.urls')),
    path('admin/', admin.site.urls),
    path('', include('api.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
