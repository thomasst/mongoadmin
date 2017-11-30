from django.conf.urls import url
from django.views.generic import RedirectView, TemplateView
from . import views

urlpatterns = (
    url(r'^$', views.СonnectsList.as_view()),
    url(r'^mongo/connect/$', views.ConnectView.as_view()),
    url(r'^mongo/connect/(?P<id>\d+)/?$', views.redirect_to),
    url(r'^mongo/(?P<connection_name>[^/]+)/$', views.ConnectionView.as_view()),
    url(r'^mongo/(?P<connection_name>[^/]+)/(?P<database_name>[^/]+)/$', views.DatabaseView.as_view()),
    url(r'^mongo/(?P<connection_name>[^/]+)/(?P<database_name>[^/]+)/(?P<collection_name>[^/]+)/$', views.CollectionView.as_view()),
    url(r'^mongo/(?P<connection_name>[^/]+)/(?P<database_name>[^/]+)/(?P<collection_name>[^/]+)/add/$', views.CreateDocumentView.as_view()),
    url(r'^mongo/(?P<connection_name>[^/]+)/(?P<database_name>[^/]+)/(?P<collection_name>[^/]+)/(?P<pk>[a-z\d]+)/$', views.UpdateDocumentView.as_view()),
    url(r'^mongo/(?P<connection_name>[^/]+)/(?P<database_name>[^/]+)/(?P<collection_name>[^/]+)/(?P<pk>[a-z\d]+)/delete/$', views.DeleteDocumentView.as_view()),
)
