# -*- coding: utf-8 -*-
import json, commands
import logging

from myhost.models import Machine_info, PhysicalMachine, VirtualMachine


def get_HostInfo(request):
    # rm -rf /tmp/ansible_info.txt && touch /tmp/ansible_info.txt && ansible $1 -m setup >> /tmp/ansible_info.txt&& rm -rf /tmp/ansible_host_linenum.txt && touch /tmp/ansible_host_linenum.txt &&cat "/tmp/ansible_info.txt" | grep -n "SUCCESS"|awk -F ':' '{print $1}' >>/tmp/ansible_host_linenum.txt;for line in `cat /tmp/ansible_host_linenum.txt`;    do      ip=`sed -n "$line"p /tmp/ansible_info.txt |awk {'print $1'}`;      result=`sed -n "$line"p /tmp/ansible_info.txt |awk {'print $3'}`;      newcontent="{\"ip\":\"$ip\",\"result\":\"$result\",";      echo $newcontent;      sed -i ""$line"s/^.*$/$newcontent/" /tmp/ansible_info.txt; done;
    physicalIp = request.POST.get('physicalIp', '')
    phyhost = PhysicalMachine.objects.filter(physicalIp=physicalIp)
    if phyhost is not None:
        (status, result) = commands.getstatusoutput('sh /tmp/test.sh %s' % physicalIp)
        if status == 0:
            all_the_text = open('/tmp/ansible_info.txt').read()
            data = json.loads(all_the_text)
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
                ip4 = []
                ip4[0] = str(data["ansible_all_ipv4_addresses"])

            except Exception, e:
                logging.error('ansible setup模块获取服务器ipv4地址数据失败:%s' % e)
                ipv4 = "未知"
        machine_info = Machine_info.objects.filter(ipv4=ip4[0], cpu_total=cpu_total, mem_total=mem_total,
                                                   cpu_type=cpu_type, disk_mount=disk_mount, disk_total=disk_total,
                                                   host_name=host_name, os_kernel=os_kernel, server_type=server_type,
                                                   swap_total=swap_total)
        if machine_info is None:
            machine_info = Machine_info(ipv4=ip4[0], cpu_total=cpu_total, mem_total=mem_total, cpu_type=cpu_type,
                                        disk_mount=disk_mount, disk_total=disk_total, host_name=host_name,
                                        os_kernel=os_kernel, server_type=server_type, swap_total=swap_total)
            machine_info.save()
