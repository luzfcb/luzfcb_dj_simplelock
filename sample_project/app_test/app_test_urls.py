from django.conf.urls import url

from . import views as app_test_views

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
        app_test_views.EditarView.as_view(),
        name='editar',
        ),
    url(r'^update2/(?P<pk>\d+)/$',
        app_test_views.EditarView2.as_view(),
        name='editar2',
        ),
]
