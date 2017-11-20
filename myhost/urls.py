from django.conf.urls import url
from .views import *
urlpatterns = [
    url(r'^phylist/$', PhyhostListView.as_view(), name = 'phyhost_list'),
    url(r'phydetail/$', PhyhostDetailView.as_view(), name = 'phyhost_detail'),
    url(r'^virlist/$', VirhostListView.as_view(), name='virhost_list'),
    url(r'virdetail/$', VirhostDetailView.as_view(), name='virhost_detail'),
]