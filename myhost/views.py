# -*- coding: utf-8 -*-

from django.views import View
from myhost.method.host import *
from myhost.method.idc import *


class IdcListView(View):
    def get(self, request):
        idc_list(request)


class IdcAddView(View):
    def post(self, request):
        idc_add(request)


class IdcDetailView(View):
    def get(self, request):
        idc_detail(request)


class IdcUpdateView(View):
    def get(self, request):
        idc_edit(request)


class HostAddView(View):
    def post(self, request):
        host_add(request)


class HostListView(View):
    def get(self, request):
        host_list(request)


class HostDetailView(View):
    def get(self, request):
        host_detail(request)


class HostUpdateView(View):
    def post(self, request):
        host_edit(request)

