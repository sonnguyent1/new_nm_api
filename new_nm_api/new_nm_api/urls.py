"""new_nm_api URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import include
from django.contrib import admin
from django.urls import path
from django.urls.conf import re_path
from django.views.generic import TemplateView
from rest_framework_jwt.views import obtain_jwt_token, verify_jwt_token, refresh_jwt_token
from tv.views import get_publish_queues, publish_queue_complete, publish_queue_dequeue


urlpatterns = [
    re_path('^presentations/', include('new_nm_api.api.urls')),
    re_path('^moo-v/', include('tv.urls')),
    re_path('^auth/token/verify/?$', verify_jwt_token),
    re_path('^auth/token/refresh/?$', refresh_jwt_token),
    re_path('^auth/token', obtain_jwt_token),
    re_path('^publishqueues/?$', get_publish_queues),
    re_path('^publishqueues/(?P<pk>\d+)/complete/?$', publish_queue_complete),
    re_path('^publishqueues/(?P<pk>\d+)/dequeue/?$', publish_queue_dequeue),
    path('', TemplateView.as_view(template_name='home.html')),
]
