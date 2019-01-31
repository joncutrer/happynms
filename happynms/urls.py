from django.conf import settings
from django.contrib import admin
from django.urls import include, path
from django.conf.urls import url

admin.site.site_title = 'happynms backend'
admin.site.site_header = 'happynms backend'
admin.site.index_title = 'grata dominus'

urlpatterns = [
    path('', include('pages.urls')),

    # Django Admin
    path('admin/', admin.site.urls),

    # User management
    path('users/', include('users.urls')),
    path('accounts/', include('allauth.urls')),

]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ]
