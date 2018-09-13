# -*- coding: utf-8 -*-
import json
import logging
import time
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, render_to_response, get_object_or_404
from django.template import RequestContext

from myhost.forms import HostForm
from myhost.models import Project, Service, Host, IDC, Server_System, SERVER_STATUS
from utils.ansible.ansible_interface import AnsiInterface


def my_render(template, data, request):
    return render_to_response(template, data, context_instance=RequestContext(request))


def host_add(request):
    """add host"""
    uf = HostForm()
    projects = Project.objects.all()
    services = Service.objects.all()
    if request.method == 'POST':
        uf_post = HostForm(request.POST)
        physics = request.POST.get('physics', '')
        ip = request.POST.get('eth0', '')
        if Host.objects.filter(eth1=ip):
            emg = u'添加失败, 该IP %s 已存在!' % ip
            return my_render('myhost:host_add', locals(), request)
        if uf_post.is_valid():
            zw = uf_post.save(commit=False)
            zw.save()
            uf_post.save_m2m()
            smg = u'主机%s添加成功!' % ip
            return render_to_response('myhost:host_list', locals(), context_instance=RequestContext(request))
    return render_to_response('myhost:host_add', locals(), context_instance=RequestContext(request))


def host_edit(request):
    """edit host"""
    uuid = request.GET.get('uuid')
    host = get_object_or_404(Host, uuid=uuid)
    uf = HostForm(instance=host)
    project_all = Project.objects.all()
    project_host = host.business.all()
    projects = [p for p in project_all if p not in project_host]
    service_all = Service.objects.all()
    service_host = host.service.all()
    services = [s for s in service_all if s not in service_host]
    username = request.user.username
    if request.method == 'POST':
        physics = request.POST.get('physics', '')
        uf_post = HostForm(request.POST, instance=host)
        if uf_post.is_valid():
            zw = uf_post.save(commit=False)
            request.POST = request.POST.copy()
            zw.save()
            uf_post.save_m2m()
            new_host = get_object_or_404(Host, uuid=uuid)
            # info = get_diff(uf_post.__dict__.get('initial'), request.POST)
            # db_to_record(username, host, info)
            # return HttpResponseRedirect('/assets/host_detail/?uuid=%s' % uuid)
            return HttpResponseRedirect('/hosts/host_detail/?uuid=%s' % uuid)
    return render_to_response('myhost:host_edit', locals(), context_instance=RequestContext(request))


def host_list(request):
    """list host"""
    hosts = Host.objects.all().order_by("-eth0")
    idcs = IDC.objects.filter()
    # lines = Line.objects.all()
    server_type = Project.objects.all()
    services = Service.objects.all()
    brands = Server_System
    server_status = SERVER_STATUS
    server_list_count = hosts.count()
    physics = Host.objects.filter(vm__isnull=True).count()
    vms = Host.objects.filter(vm__isnull=False).count()
    # contact_list, p, contacts, page_range, current_page, show_first, show_end = pages(hosts, request)
    return render(request, 'host_list.html', {'hosts': hosts})


def host_detail(request):
    """host detail"""
    uuid = request.GET.get('uuid', '')
    ip = request.GET.get('ip', '')
    if uuid:
        host = get_object_or_404(Host, uuid=uuid)
    elif ip:
        host = get_object_or_404(Host, eth0=ip)
    # host_record = HostRecord.objects.filter(host=host).order_by('-time')
    # return render_to_response('host_detail.html', locals(), context_instance=RequestContext(request))
    return render(request, 'host_detail.html', {'host': host})


def getHostInfo(hostname, port, username, password, ip):
    hostname = hostname
    port = port
    username = username
    password = password
    ip = ip
    resource = [{"hostname": hostname, "port": port, "username": username, "password": password,
                 "ip": ip}]
    interface = AnsiInterface(resource)
    data = interface.exec_setup([ip])
    data = json.loads(data)
    data = data["success"]
    try:
        data = data["ansible_facts"]
    except Exception, e:
        logging.error('ansible setup模块获取数据失败:%s' % e)
        return "error"
        # 主机名 node_name
    try:
        node_name = data["ansible_nodename"]
    except Exception, e:
        logging.error('ansible setup模块获取node_name数据失败:%s' % e)
        node_name = "未知"
        # 网卡eth0
    try:
        eth0 = data["ansible_eth0"]["ipv4"]["address"]
    except Exception, e:
        logging.error('ansible setup模块获取网卡eth0数据失败:%s' % e)
        eth0 = "未知"
        # 网卡eth1
    try:
        eth1 = data["ansible_eth1"]["ipv4"]["address"]
    except Exception, e:
        logging.error('ansible setup模块获取网卡eth1数据失败:%s' % e)
        eth1 = "未知"
        # MAC地址
    try:
        mac = data["ansible_default_ipv4"]["macaddress"]
    except Exception, e:
        logging.error('ansible setup模块获取网mac数据失败:%s' % e)
        mac = "未知"
        # CPU型号
    try:
        cpu_total = data["ansible_processor_vcpus"]
        cpu_type = data["ansible_processor"][-1]
        cpu = str(cpu_type) + " | " + str(cpu_total + "核")
    except Exception, e:
        logging.error('ansible setup模块获取CPU数据失败:%s' % e)
        cpu = "未知"
        # 硬盘总容量
    try:
        hard_disk = str(sum([int(data["ansible_devices"][i]["sectors"]) * int(
            data["ansible_devices"][i]["sectorsize"]) / 1024 / 1024 / 1024 \
                             for i in data["ansible_devices"] if i[0:2] in ("sd", "ss")])) + "G"
    except Exception, e:
        logging.error('ansible setup模块获取硬盘总容量数据失败:%s' % e)
        hard_disk = 0
        # 物理内存容量
    try:
        mem_total_mb = data["ansible_memtotal_mb"]
        mem_total = str(int(mem_total_mb) / 1024) + "G"
    except Exception, e:
        logging.error('ansible setup模块获取物理内存容量数据失败:%s' % e)
        mem_total = 0

        # 系统
    try:
        system = " ".join((data["ansible_distribution"], data["ansible_distribution_version"]))
    except Exception, e:
        logging.error('ansible setup模块获取操作系统数据失败:%s' % e)
        system = "未知"

        # 当前时间
    try:
        create_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    except Exception, e:
        logging.error('ansible setup模块获取创建时间失败:%s' % e)
        create_time = "未知"

        # 主机类型
    try:
        ansible_virtualization_type = data["ansible_virtualization_type"]
        if ansible_virtualization_type == "NA":
            type = "物理机"
        else:
            type = "虚拟机"
    except Exception, e:
        logging.error('ansible setup模块获取主机类型失败:%s' % e)
        type = "未知"
        # 端口
    try:
        ssh_connection = data["ansible_env"]["SSH_CONNECTION"]
        switch_port = ssh_connection.split(" ")[3]
    except Exception, e:
        logging.error('ansible setup模块获取端口失败:%s' % e)
        switch_port = "未知"
    # 硬盘挂载名及容量
    try:
        disk_mount = json.dumps([{"mount": i["mount"], "size": i["size_total"] / 1024 / 1024 / 1024} for i in
                                 data["ansible_mounts"]])
    except Exception, e:
        logging.error('ansible setup模块获取硬盘挂载名及容量数据失败:%s' % e)
        disk_mount = "未知"

    result = {}
    result = {'node_name': node_name, 'eth0': eth0, 'eth1': eth1, 'mac': mac, 'cpu': cpu, 'hard_disk': hard_disk,
              'mem_total': mem_total, 'system': system, 'create_time': create_time, 'type': type,
              'switch_port': switch_port, 'disk_mount': disk_mount}
    print result.get("disk_mount")
    return result


def getHostInfo_ajax(request):
    if request.method == "GET":
        physicalIp = request.GET.get("physicalIp_input")
        machine_info = getHostInfo(physicalIp)
        return HttpResponse(json.dumps({"machine_info_str": machine_info}))
    return render(request, 'error_500.html')


if __name__ == '__main__':
    # resource = [{"hostname": "172.16.251.114", "port": "1221", "username": "lishide", "password": "lishide",
    #              "ip": '172.16.251.114'}
    getHostInfo("123.103.74.8", "1221", "test", "test", "123.103.74.8")
