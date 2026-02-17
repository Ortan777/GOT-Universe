from django.contrib import admin
from django.urls import path, include

from .views import home, analytics_dashboard
from .search_views import global_search

urlpatterns = [
    path('', home, name='home'),

    path('admin/', admin.site.urls),
    path('analytics/', analytics_dashboard, name='analytics_dashboard'),

    path('houses/', include('houses.urls')),
    path('characters/', include('characters.urls')),
    path('locations/', include('locations.urls')),
    path('events/', include('events.urls')),

    path('search/', global_search, name='global_search'),
]
