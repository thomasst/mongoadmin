from django.conf.urls.defaults import *

from . import views

urlpatterns = patterns('mongoadmin',
    url(r'^mongo/(?P<connection_name>[^/]+)/$', views.ConnectionView.as_view()),
    url(r'^mongo/(?P<connection_name>[^/]+)/(?P<database_name>[^/]+)/$', views.DatabaseView.as_view()),
    url(r'^mongo/(?P<connection_name>[^/]+)/(?P<database_name>[^/]+)/(?P<collection_name>[^/]+)/$', views.CollectionView.as_view()),
    url(r'^mongo/(?P<connection_name>[^/]+)/(?P<database_name>[^/]+)/(?P<collection_name>[^/]+)/new/$', views.CreateDocumentView.as_view()),
    url(r'^mongo/(?P<connection_name>[^/]+)/(?P<database_name>[^/]+)/(?P<collection_name>[^/]+)/(?P<pk>[a-z\d]+)/$', views.UpdateDocumentView.as_view()),
)
