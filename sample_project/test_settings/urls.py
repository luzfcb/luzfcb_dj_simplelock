"""sample_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from luzfcb_dj_simplelock import views
from app_test import views as app_test_views

urlpatterns = [
    url(r'^$',
        app_test_views.PersonList.as_view(),
        name='list',
        ),
    url(r'^create/$',
        app_test_views.PersonCreate.as_view(),
        name='create'
        ),
    url(r'^detail/(?P<pk>\d+)/$',
        app_test_views.PersonDetail.as_view(),
        name='detail'
        ),

    url(r'^update/(?P<pk>\d+)/$',
        views.editar,
        name='editar'
        ),
    url(r'^admin/', admin.site.urls),
]
