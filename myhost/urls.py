from django.conf.urls import url
from .views import *

urlpatterns = [
    url(r'^idc_add/', IdcAddView.as_view(), name='idc_add'),
    url(r'^idc_list/', IdcListView.as_view(), name='idc_list'),
    url(r'^idc_detail/(?P<uuid>\d+)/$', IdcDetailView.as_view(), name='idc_detail'),
    url(r'^idc_update/', IdcUpdateView.as_view(), name='idc_update'),
    url(r'^host_add/', HostAddView.as_view(), name='host_add'),
    url(r'^host_list/', HostListView.as_view(), name='host_list'),
    url(r'^host_detail/(?P<uuid>\d+)/$', HostDetailView.as_view(), name='host_detail'),
    url(r'^host_update/', HostUpdateView.as_view(), name='host_update'),
    # url(r'^cancelphy/$', CancelPhyHostView.as_view, name='cancelphy'),
    # url(r'^addphy/$', AddPhyHostView.as_view(), name='addphy'),
    # url(r'^phydetail/(?P<physicalIp>\d+)/$', PhyhostDetailView.as_view(), name='phyhost_detail'),
    # url(r'^virlist/$', VirhostListView.as_view(), name='virhost_list2'),
    # url(r'^addvir/$', AddVirHostView.as_view(), name='addvir'),
    # url(r'virdetail/(?P<virtualIp>\d+)/$', VirhostDetailView.as_view(), name='virhost_detail'),
    # url(r'^viralllist/$', VirhostList_allView.as_view(), name='virhost_list'),
]
