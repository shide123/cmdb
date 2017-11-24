from django.conf.urls import url
from .views import *

urlpatterns = [
    url(r'^machineinfo/$', getHostInfo_ajax, name='machineinfo'),
    url(r'^phylist/$', PhyhostListView.as_view(), name='phyhost_list'),
    url(r'^delphy/$', DelPhyHostView.as_view, name='delphy'),
    url(r'^cancelphy/$', CancelPhyHostView.as_view, name='cancelphy'),
    url(r'^addphy/$', AddPhyHostView.as_view(), name='addphy'),
    url(r'^phydetail/(?P<physicalIp>\d+)/$', PhyhostDetailView.as_view(), name='phyhost_detail'),
    url(r'^virlist/$', VirhostListView.as_view(), name='virhost_list2'),
    url(r'^addvir/$', AddVirHostView.as_view(), name='addvir'),
    url(r'virdetail/(?P<virtualIp>\d+)/$', VirhostDetailView.as_view(), name='virhost_detail'),
    url(r'^viralllist/$', VirhostList_allView.as_view(), name='virhost_list'),
]
