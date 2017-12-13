# -*- coding: utf-8 -*-
from django import forms
from myhost.models import *


class HostForm(forms.ModelForm):
    class Meta:
        model = Host
        # "guarantee_date" --待定
        fields = ["node_name", "idc", "eth0", "eth1", "mac", "disk_mount",
                  "number", "business", "env", "status",
                  "cpu", "hard_disk", "memory", "system", "vm",
                  "brand", "idle", "editor"]


class IdcForm(forms.ModelForm):
    class Meta:
        model = IDC
        fields = ['name', "bandwidth", "operator", 'type', 'linkman', 'phone', 'network', 'address', 'comment']


class Project_docForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ["description"]


class ServiceForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = ['name', 'port', 'remark']
