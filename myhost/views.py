# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.http import HttpResponseRedirect
from pure_pagination import PageNotAnInteger, EmptyPage, Paginator
from django.views.generic.base import View
from myhost.models import *
from myhost.forms import *
from django.shortcuts import render
import json, commands
import logging

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
    def get(self, request, physicalIp):
        phyhost = PhysicalMachine.objects.get(physicalIp=physicalIp)
        return render(request, 'phyhost_detail.html', {'phyhost', phyhost})


class VirhostList_allView(View):
    def get(self, request):
        #all_virtual = VirtualMachine.objects.all().order_by("virtualIp")
        #try:
        #    page = request.GET.get('page', 1)
        #except PageNotAnInteger:
        #    page = 1
        #p = Paginator(all_virtual, 3, request=request)
        #virtual_list = p.page(page)
        #return render(request, 'myVirHost.html', {'all_virtual', virtual_list})
        return render(request, 'myVirHost.html')

class VirhostListView(View):
    def get(self, request, physicalIp):
        physical = PhysicalMachine.objects.get(physicalIp=physicalIp)
        all_virtual = VirtualMachine.objects.get(PhysicalMachine=physical)
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(all_virtual, 3, request=request)
        virtual_list = p.page(page)
        return render(request, 'myVirHost.html', {'all_virtual', virtual_list})


class VirhostDetailView(View):
    def get(self, request, virtualIp):
        virhost = PhysicalMachine.objects.get(virtualIp=virtualIp)
        return render(request, 'virhost_detail.html', {'virhost', virhost})


class AddPhyHostView(View):
    def get(self, request):
        phy_forms = PhysicalForm()
        return render(request, 'phyhost_forms.html', {'phy_forms': phy_forms})

    def post(self, request):
        phy_forms = PhysicalForm(request.POST)
        if phy_forms.is_valid():
            physicalIp = request.POST.get('physicalIp', '')
            machineRoom_address = request.POST.get('machineRoom_address', '')
            machineRoom_attr = request.POST.get('machineRoom_attr', '')
            machine_info = request.POST.get('machine_info', '')
            phyhost = PhysicalMachine.objects.filter(physicalIp=physicalIp, machineRoom_address=machineRoom_address, machineRoom_attr=machineRoom_attr)
            if phyhost is not None:
                phyhost.save()
                return HttpResponseRedirect('/hosts/phylist/')

class GetPhyHostInfoView(View):
    def post(self, request):
        return
    def get(self, request):
        return


class AddVirHostView(View):
    def get(self, request):
        return 0

    def post(self, request):
        return 0


class UpdatePhyHostView(View):
    def get(self, request, physicalIp):
        return 0

    def post(self, request):
        return 0


class UpdateVirHostView(View):
    def get(self, request):
        return 0

    def post(self, request):
        return 0
