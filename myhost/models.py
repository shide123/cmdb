# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.
class Machine_info(models.Model):
    mem_total = models.CharField(max_length=20, default='unknown')
    swap_total = models.CharField(max_length=20, default='unknown')
    cpu_type = models.CharField(max_length=20, default='unknown')
    cpu_total = models.IntegerField(default=0)
    os_type = models.CharField(max_length=20, default='unknown')
    disk_total = models.CharField(max_length=20, default='unknown')
    disk_mount = models.CharField(max_length=20, default='unknown')
    server_type = models.CharField(max_length=20, default='unknown')
    host_name = models.CharField(max_length=20, default='unknown')
    os_kernel = models.CharField(max_length=20, default='unknown')
    ipv4 = models.CharField(max_length=20, default='unknown')

class PhysicalMachine(models.Model):
    physicalIp = models.CharField(max_length=16)
    machineRoom_address = models.CharField(max_length=8)
    machineRoom_attr = models.CharField(max_length=10)
    machine_info = models.OneToOneField(Machine_info)



class VirtualMachine(models.Model):
    virtualIp = models.CharField(max_length=16)
    process_info = models.TextField(max_length=10240)
    note = models.TextField(max_length=10240)
    physicalMachine = models.ForeignKey(PhysicalMachine)
