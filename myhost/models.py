# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from django.db.models import UUIDField

idc_operator = (
    (0, u"电信"),
    (1, u"联通"),
    (2, u"移动"),
    (3, u"铁通"),
    (4, u"小带宽"),
)
idc_type = (
    (0, u"CDN"),
    (1, u"核心")
)
system_arch = [(u"x86_64", u"x86_64")]

Server_System = [
    (i, i) for i in
    (
        u"Dell R210",
        u"Dell R410",
        u"Dell R420",
        u"Dell R510",
        u"Dell R620",
        u"Dell R710",
        u"Dell R720",
        u"Dell R720xd",
        u"Dell R730xd",
        u"HP",
        u"HP DL360p",
        u"HP DL380e",
        u"HP DL160",
        u"Lenovo",
        u"Lenovo WQ R510 G7",
        u"Lenovo ThinkServer RD330",
        u"Lenovo ThinkServer RD340",
        u"DIY",
        u"VIP",
        u"虚拟化",
        u"Other",
        u"MediaServer",
        u"网络设备",
    )
]
SERVER_STATUS = (
    (0, u"未安装系统"),
    (1, u"已安装系统"),
    (2, u"正在安装系统"),
    (3, u"报废"),
)
System_os = [(i, i) for i in (u"CentOS", u"Windows")]
BOOL_CHOICES = ((True, '使用中'), (False, '空闲'))
ENVIRONMENT = [(i, i) for i in (u"st", u"aws", u"prod", u"pub")]
room_hours = [(u"3-2", u"3-2")]


class IDC(models.Model):
    uuid = UUIDField(primary_key=True)
    name = models.CharField(max_length=64, verbose_name=u'机房名称')
    bandwidth = models.CharField(max_length=64, blank=True, null=True, verbose_name=u'机房带宽')
    phone = models.CharField(max_length=32, verbose_name=u'联系电话')
    linkman = models.CharField(max_length=32, null=True, verbose_name=u'联系人')
    address = models.CharField(max_length=128, blank=True, null=True, verbose_name=u"机房地址")
    network = models.TextField(blank=True, null=True, verbose_name=u"IP地址段")
    create_time = models.DateField(auto_now=True)
    operator = models.IntegerField(verbose_name=u"运营商", choices=idc_operator, max_length=32, blank=True, null=True)
    type = models.IntegerField(verbose_name=u"机房类型", choices=idc_type, max_length=32, blank=True, null=True)
    comment = models.TextField(blank=True, null=True, verbose_name=u"备注")

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = u"IDC机房"
        verbose_name_plural = verbose_name


class Host(models.Model):
    uuid = UUIDField(auto=True, primary_key=True)
    node_name = models.CharField(max_length=100, blank=True, null=True, verbose_name=u"主机名")
    idc = models.ForeignKey(IDC, blank=True, null=True, verbose_name=u'机房', on_delete=models.SET_NULL)
    eth1 = models.IPAddressField(blank=True, null=True, verbose_name=u'网卡1')
    eth2 = models.IPAddressField(blank=True, null=True, verbose_name=u'网卡2')
    mac = models.CharField(max_length=20, blank=True, null=True, verbose_name=u"MAC")
    brand = models.CharField(max_length=64, choices=Server_System, blank=True, null=True, verbose_name=u'硬件厂商')
    cpu = models.CharField(max_length=64, blank=True, null=True, verbose_name=u'CPU')
    hard_disk = models.CharField(max_length=128, blank=True, null=True, verbose_name=u'硬盘')
    memory = models.CharField(max_length=128, blank=True, null=True, verbose_name=u'内存')
    system = models.CharField(verbose_name=u"系统类型", max_length=32, choices=System_os, default="CentOS", blank=True,
                              null=True, )
    system_cpuarch = models.CharField(max_length=32, blank=True, null=True, choices=system_arch, verbose_name=u"系统版本")
    system_version = models.CharField(max_length=8, blank=True, null=True, verbose_name=u"版本号")
    create_time = models.DateTimeField(auto_now_add=True)
    server_cabinet_id = models.IntegerField(blank=True, null=True, verbose_name=u'机器位置')
    number = models.CharField(max_length=32, blank=True, null=True, verbose_name=u'资产编号')
    editor = models.TextField(blank=True, null=True, verbose_name=u'备注')
    # business = models.ManyToManyField(Project, blank=True, null=True, verbose_name=u'所属业务')
    u"""
    0   未安装系统
    1   已安装系统
    2   正在安装中
    3   报废
    """
    # status = models.IntegerField(verbose_name=u"机器状态", choices=SERVER_STATUS, default=0, blank=True)
    vm = models.ForeignKey("self", blank=True, null=True, verbose_name=u"虚拟机父主机")
    type = models.IntegerField(verbose_name=u'主机类型', default=1, blank=True, max_length=2)
    Services_Code = models.CharField(max_length=16, blank=True, null=True, verbose_name=u"快速服务编码")
    env = models.CharField(max_length=32, blank=True, null=True, verbose_name=u"环境", choices=ENVIRONMENT)
    room_number = models.CharField(verbose_name=u"房间号", max_length=32, choices=room_hours, blank=True, null=True)
    server_sn = models.CharField(verbose_name=u"SN编号", max_length=32, blank=True, null=True)
    switch_port = models.CharField(verbose_name=u"端口号", max_length=12, blank=True, null=True)
    # service = models.ManyToManyField(Service, verbose_name=u'运行服务', blank=True, null=True)
    idle = models.BooleanField(verbose_name=u'状态', default=1, choices=BOOL_CHOICES)

    def __unicode__(self):
        return self.node_name

    class Meta:
        verbose_name = u"服务器"
        verbose_name_plural = verbose_name
