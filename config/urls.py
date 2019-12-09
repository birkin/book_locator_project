# -*- coding: utf-8 -*-

from django.conf.urls import include, url
from django.contrib import admin
from django.views.generic import RedirectView
from book_locator_app import views


admin.autodiscover()


urlpatterns = [

    # url( r'^admin/', admin.site.urls ),

    # url( r'^admin/login/', RedirectView.as_view(pattern_name='login_url') ),

    url( r'^map/', views.map, name='map_url' ),

    url( r'^print_labels/(?P<location_code>.*)/$', views.labels_print, name='labels_print_url' ),
    url( r'^print_labels/', views.labels_home, name='labels_home_url' ),

    url( r'^info/', views.info, name='info_url' ),

    url( r'^version/$', views.version, name='version_url' ),

    url( r'^error_check/$', views.error_check, name='error_check_url' ),

    # url( r'^login/$', views.login, name='login_url' ),

    url( r'^$', RedirectView.as_view(pattern_name='info_url') ),

    ]
