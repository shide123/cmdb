# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from pure_pagination import PageNotAnInteger, EmptyPage, Paginator
from django.views.generic.base import View
from myhost.models import *

from django.shortcuts import render

# Create your views here.
class PhyhostListView(View):
    def get(self, request):
        all_physical = PhysicalMachine.objects.all().order_by("physicalIp")

        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(all_physical, 3, request=request)
        physicals_list = p.page(page)
        return render(request, 'myHost.html', {
            'all_physical': physicals_list,
        })

class PhyhostDetailView(View):
    def get(self, request, phyhost_id):
        phyhost = PhysicalMachine.objects.get(id=int(phyhost_id))
        return render(request, '',{})

    def post(self, request):


         return 0

class VirhostListView(View):
    def get(self, request,virhost_id):

        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
            #p = Paginator
        return 0



class VirhostDetailView(View):
    def get(self, request):
        all_physical = PhysicalMachine.objects.all().order_by("physicalIp")

        return 0








class UpdatePhyHostView(View):
    def get(self, request):

        return 0
    def post(self, request):
        return 0

class UpdateVirHostView(View):
    def get(self, request):
        return 0
    def post(self, request):
        return 0

class AddPhyHostView(View):
    def get(self, request):

        return 0
    def post(self, request):
        return 0

class AddVirHostView(View):
    def get(self, request):
        return 0
    def post(self, request):
        return 0
