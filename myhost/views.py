# -*- coding: utf-8 -*-
import json
import logging
import time
from django.http import HttpResponse
from django.shortcuts import render
from django.views import View
from myhost.method.idc import *
from myhost.method.host import *
from utils.ansible.ansible_interface import AnsiInterface


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

# class VirhostList_allView(View):
#     def get(self, request):
#         all_virtual = VirtualMachine.objects.all().order_by("virtualIp")
#         try:
#             page = request.GET.get('page', 1)
#         except PageNotAnInteger:
#             page = 1
#         p = Paginator(all_virtual, 3, request=request)
#         virtual_list = p.page(page)
#         return render(request, 'myVirHost.html', {'all_virtual', virtual_list})
#         return render(request, 'myVirHost.html')
#
#
# class VirhostListView(View):
#     def get(self, request, physicalIp):
#         physical = PhysicalMachine.objects.get(physicalIp=physicalIp)
#         all_virtual = VirtualMachine.objects.get(PhysicalMachine=physical)
#         try:
#             page = request.GET.get('page', 1)
#         except PageNotAnInteger:
#             page = 1
#         p = Paginator(all_virtual, 3, request=request)
#         virtual_list = p.page(page)
#         return render(request, 'myVirHost.html', {'all_virtual', virtual_list})
#
#
# class VirhostDetailView(View):
#     def get(self, request, virtualIp):
#         virhost = PhysicalMachine.objects.get(virtualIp=virtualIp)
#         return render(request, 'virhost_detail.html', {'virhost', virhost})
#
#
# class AddPhyHostView(View):
#     def get(self, request):
#         return render(request, 'phyhost_forms.html')
#
#     def post(self, request):
#         phy_forms = PhysicalForm(request.POST)
#         if phy_forms.is_valid():
#             physicalIp_input = request.POST.get('physicalIp_input', '')
#             machineRoom_address = request.POST.get('machineRoom_address', '')
#             machineRoom_attr = request.POST.get('machineRoom_attr', '')
#             machine_info_json = getHostInfo(physicalIp_input)
#             machine_info_json = json.loads(machine_info_json)
#             ipv4 = machine_info_json[0]["fields"]["ipv4"]
#             cursor = connection.cursor()
#             machine_id = cursor.execute("select id from myhost_machine_info where ipv4=%s", [ipv4])
#             # virtualMachine_ip = request.POST.get('virtualMachine_ip', '')
#             # virip_arr = virtualMachine_ip.split(',')
#             # physicalmachine = PhysicalMachine.objects.filter(physicalIp=physicalIp_input)
#             # for l in range(len(virip_arr)):
#             # VirtualMachine.objects.filter(virtualIp=virip_arr[l]).update(physicalMachine=physicalmachine)
#             #    cursor.execute("update set myhost_virtualmachine where physica")
#             if machine_id:
#                 dic = {'physicalIp': physicalIp_input, 'machineRoom_address': machineRoom_address,
#                        'machineRoom_attr': machineRoom_attr, 'machine_info_id': machine_id}
#                 PhysicalMachine.objects.create(**dic)
#                 response = HttpResponsePermanentRedirect(reversed('myhost:phyhost_list'))
#                 return response
#             else:
#                 return render(request, 'error_500.html')
#         return render(request, 'error_500.html')


# class DelPhyHostView(View):
#     def get(self, request):
#         physicalIp_input = request.POST.get('physicalIp_input', '')
#         PhysicalMachine.objects.filter(physicalIp=physicalIp_input).delete()
#         return render(request, 'myhost:phyhost_list')
#
#
# class CancelPhyHostView(View):
#     def get(self, request):
#         return render(request, 'myhost:phyhost_list')
#
#
# class AddVirHostView(View):
#     def get(self, request):
#         return render(request, 'virhost_forms.html')
#
#     def post(self, request):
#         virform = VirtualForm(request.POST)
#         if virform.is_valid():
#             virtualIp = request.POST.get('virtualIp', '')
#             physicalIp = request.POST.get('physicalIp', '')
#             note = request.POST.get('note', '')
#             process_info = request.POST.get('process_info', '')
#             cursor = connection.cursor()
#             phyHost = PhysicalMachine.objects.filter(physicalIp=physicalIp)
#             physicalId = cursor.execute("select id from myhost_physicalmachine where physicalIp=%s", [physicalIp])
#             virtualmachine = VirtualMachine.objects.filter(virtualIp=virtualIp)
#             if virtualmachine:
#                 logging.info("exit virhost")
#                 return render(request, 'virhost_forms.html')
#             else:
#                 dic = {'virtualIp': virtualIp, 'process_info': process_info, 'note': note, 'physicalId': physicalId}
#                 VirtualMachine.save(**dic)
#                 all_vir = VirtualMachine.objects.all()
#                 return render(request, 'myVirHost.html', {'all_vir': all_vir})
#         else:
#             return render(request, 'virhost_forms.html')
