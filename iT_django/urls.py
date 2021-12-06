#iT_django URL Configuration

from django.contrib import admin
from django.urls import path, re_path, include
from django.contrib.auth import views as auth_views

from django.conf import settings
from django.conf.urls.i18n import i18n_patterns
from django.conf.urls.static import static

from django.views.static import serve 

from django.conf.urls import handler404, handler500
     
#handler404 = "mainapp.views.handler_404"
#handler500 = "mainapp.views.handler_500"

urlpatterns = [

    path('ckeditor/', include('ckeditor_uploader.urls')),

    path("", include('mainapp.urls')),

    path('i18n/', include('django.conf.urls.i18n')),

    re_path(r'^media/(?P<path>.*)$', serve,{'document_root': settings.MEDIA_ROOT}), 
    re_path(r'^static/(?P<path>.*)$', serve,{'document_root': settings.STATIC_ROOT}),

]

urlpatterns += i18n_patterns(
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('pages/', include('django.contrib.flatpages.urls')),
)