from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from core.views import HomeView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', HomeView.as_view(), name='home'),
    path('', include('core.urls')),
    path('characters/', include('characters.urls')),
    path('houses/', include('houses.urls')),
    path('map/', include('map.urls')),  # This should be here
    path('timeline/', include('timeline.urls')),
    path('api/', include('characters.urls_api')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)