"""celerymonitor URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import include, url
from django.contrib import admin
from django.urls import path
from monitor.views import WorkersIndexView
from django.contrib.auth import login, logout
from rest_framework.authtoken.views import obtain_auth_token
from monitor.views import CustomLoginView


urlpatterns = [
    path("admin", admin.site.urls),
    path("accounts/login/", CustomLoginView.as_view(), name="login"),
    path("accounts/logout/", logout, name="logout"),
    path(r"monitor/", include("monitor.urls")),
    path("", WorkersIndexView.as_view()),
    path("api-auth", include("rest_framework.urls", namespace="rest_framework")),
    path("api-token-auth/", obtain_auth_token),
    # url(r'^grappelli/', include('grappelli.urls')),
]


try:
    from .extend_urls import extend_urlpatterns

    urlpatterns = urlpatterns + extend_urlpatterns
except ImportError:
    pass
