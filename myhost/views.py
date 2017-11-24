# -*- coding: utf-8 -*-
from django.core import serializers
from django.http import HttpResponseRedirect, HttpResponsePermanentRedirect, response, HttpResponse
from pure_pagination import PageNotAnInteger, EmptyPage, Paginator
from django.views.generic.base import View
from myhost.forms import *
from django.shortcuts import render
import json, commands
import logging
from django.db import connection


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
        all_virtual = VirtualMachine.objects.all().order_by("virtualIp")
        try:
           page = request.GET.get('page', 1)
        except PageNotAnInteger:
           page = 1
        p = Paginator(all_virtual, 3, request=request)
        virtual_list = p.page(page)
        return render(request, 'myVirHost.html', {'all_virtual', virtual_list})
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
        return render(request, 'phyhost_forms.html')

    def post(self, request):
        phy_forms = PhysicalForm(request.POST)
        if phy_forms.is_valid():
            physicalIp_input = request.POST.get('physicalIp_input', '')
            machineRoom_address = request.POST.get('machineRoom_address', '')
            machineRoom_attr = request.POST.get('machineRoom_attr', '')
            machine_info_json = getHostInfo(physicalIp_input)
            machine_info_json = json.loads(machine_info_json)
            ipv4 = machine_info_json[0]["fields"]["ipv4"]
            cursor = connection.cursor()
            machine_id = cursor.execute("select id from myhost_machine_info where ipv4=%s", [ipv4])
            # virtualMachine_ip = request.POST.get('virtualMachine_ip', '')
            # virip_arr = virtualMachine_ip.split(',')
            # physicalmachine = PhysicalMachine.objects.filter(physicalIp=physicalIp_input)
            # for l in range(len(virip_arr)):
            # VirtualMachine.objects.filter(virtualIp=virip_arr[l]).update(physicalMachine=physicalmachine)
            #    cursor.execute("update set myhost_virtualmachine where physica")
            if machine_id:
                dic = {'physicalIp': physicalIp_input, 'machineRoom_address': machineRoom_address,
                       'machineRoom_attr': machineRoom_attr, 'machine_info_id': machine_id}
                PhysicalMachine.objects.create(**dic)
                return render(request, 'myhost:phyhost_list')
            else:
                return render(request, 'error_500.html')
        return render(request, 'error_500.html')


def getHostInfo_ajax(request):
    if request.method == "GET":
        physicalIp = request.GET.get("physicalIp_input")
        machine_info = getHostInfo(physicalIp)
        return HttpResponse(json.dumps({"machine_info_str": machine_info}))
    return render(request, 'error_500.html')


def getHostInfo(physicalIp):
    (status, result) = commands.getstatusoutput('sh /tmp/test.sh %s' % physicalIp)
    if status == 0:
        all_the_text = open('/tmp/ansible_info.txt').read()
        data = json.loads(all_the_text)
        ip4 = []
        machine_info_str = ""
        try:
            data = data["ansible_facts"]
        except Exception, e:
            logging.error('ansible setup模块获取数据失败:%s' % e)
            return "error"
            # 物理内存容量
        try:
            mem_total = data["ansible_memtotal_mb"]
        except Exception, e:
            logging.error('ansible setup模块获取物理内存容量数据失败:%s' % e)
            mem_total = 0
            # 虚拟内容容量
        try:
            swap_total = data["ansible_memory_mb"]["swap"]["total"]
        except Exception, e:
            logging.error('ansible setup模块获取虚拟内容容量数据失败:%s' % e)
            swap_total = 0
            # CPU型号
        try:
            cpu_type = data["ansible_processor"][-1]
        except Exception, e:
            logging.error('ansible setup模块获取CPU型号数据失败:%s' % e)
            cpu_type = "未知"
            # CPU核心数
        try:
            cpu_total = data["ansible_processor_vcpus"]
        except Exception, e:
            logging.error('ansible setup模块获取CPU核心数数据失败:%s' % e)
            cpu_total = 0
            # 操作系统类型
        try:
            os_type = " ".join((data["ansible_distribution"], data["ansible_distribution_version"]))
        except Exception, e:
            logging.error('ansible setup模块获取操作系统类型数据失败:%s' % e)
            os_type = "未知"
            # 硬盘总容量
        try:
            disk_total = sum([int(data["ansible_devices"][i]["sectors"]) * \
                              int(data["ansible_devices"][i]["sectorsize"]) / 1024 / 1024 / 1024 \
                              for i in data["ansible_devices"] if i[0:2] in ("sd", "ss")])
        except Exception, e:
            logging.error('ansible setup模块获取硬盘总容量数据失败:%s' % e)
            disk_total = 0
            # 硬盘挂载名及容量
        try:
            disk_mount = str(
                [{"mount": i["mount"], "size": i["size_total"] / 1024 / 1024 / 1024} for i in
                 data["ansible_mounts"]])
        except Exception, e:
            logging.error('ansible setup模块获取硬盘挂载名及容量数据失败:%s' % e)
            disk_mount = "未知"
            # 服务器型号
        try:
            server_type = data["ansible_product_name"]
        except Exception, e:
            logging.error('ansible setup模块获取服务器型号数据失败:%s' % e)
            server_type = "未知"
            # 服务器主机名
        try:
            host_name = data["ansible_hostname"]
        except Exception, e:
            logging.error('ansible setup模块获取服务器主机名数据失败:%s' % e)
            host_name = "未知"
            # 操作系统内核型号
        try:
            os_kernel = data["ansible_kernel"]
        except Exception, e:
            logging.error('ansible setup模块获取操作系统内核型号数据失败:%s' % e)
            os_kernel = "未知"
            # 服务器ipv4地址
        try:
            ip4 = data["ansible_all_ipv4_addresses"]

        except Exception, e:
            logging.error('ansible setup模块获取服务器ipv4地址数据失败:%s' % e)
            #         ip4 = "未知"
        machine_info = Machine_info.objects.filter(ipv4=ip4, cpu_total=cpu_total, mem_total=mem_total,
                                                   cpu_type=cpu_type, disk_mount=disk_mount,
                                                   disk_total=disk_total,
                                                   host_name=host_name, os_kernel=os_kernel,
                                                   server_type=server_type,
                                                   swap_total=swap_total)
        if machine_info:
            logging.info("exist machine info")
        else:
            dic = {'ipv4': ip4, 'cpu_total': cpu_total, 'mem_total': mem_total,
                   'cpu_type': cpu_type,
                   'disk_mount': disk_mount, 'disk_total': disk_total, 'host_name': host_name,
                   'os_kernel': os_kernel, 'server_type': server_type, 'swap_total': swap_total}
            Machine_info.objects.create(**dic)
        machine_info = serializers.serialize('json', machine_info)
    return machine_info


class DelPhyHostView(View):
    def get(self, request):
        physicalIp_input = request.POST.get('physicalIp_input', '')
        PhysicalMachine.objects.filter(physicalIp=physicalIp_input).delete()
        return render(request, 'myhost:phyhost_list')


class CancelPhyHostView(View):
    def get(self, request):
        return render(request, 'myhost:phyhost_list')


# do
class AddVirHostView(View):
    def get(self, request):
        return render(request, 'virhost_forms.html')

    def post(self, request):
        virform = VirtualForm(request.POST)
        if virform.is_valid():
            virtualIp = request.POST.get('virtualIp', '')
            physicalIp = request.POST.get('physicalIp', '')
            note = request.POST.get('note', '')
            process_info = request.POST.get('process_info', '')
            cursor = connection.cursor()
            phyHost = PhysicalMachine.objects.filter(physicalIp=physicalIp)
            physicalId = cursor.execute("select id from  myhost_physicalmachine where physicalIp=%s", [physicalIp])
            phyHost
            virtualmachine = VirtualMachine.objects.filter(virtualIp=virtualIp)
            if virtualmachine:
                logging.info("exit virhost")
                return render(request, 'myhost:addvir')
            else:
                dic = {'virtualIp': virtualIp, 'process_info': process_info, 'note': note, 'physicalId': physicalId}
                VirtualMachine.save(**dic)
                return render(request, 'myhost:viralllist')
        else:
            return render(request, 'myhost:addvir')


