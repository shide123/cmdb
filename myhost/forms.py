# -*- coding: utf-8 -*-
from django import forms
from myhost.models import *

from myhost.models import VirtualMachine


class PhysicalForm(forms.Form):
    physicalIp = forms.CharField(required=True)
    machineRoom_address = forms.CharField(required=True)
    machineRoom_attr = forms.CharField(required=True)
    machine_info = forms.OneToOneField(required=True)
    selectphysicalMachine = PhysicalMachine.objects.filter(physicalIp=physicalIp)
    if selectphysicalMachine:
        id = selectphysicalMachine.id
    virtualMachineModel = VirtualMachine.objects.filter(physicalMachine=selectphysicalMachine)
    virtualMachine_List = []
    for i in virtualMachineModel:
        v = []
        v.append(i.virtualIp)
        virtualMachine_List.append(v)
    virtualMachine_ip = forms.MultipleChoiceField(choices=virtualMachine_List, widget=forms.CheckboxSelectMultiple(),
       required=False)

class VirtualForm(forms.Form):
    virtualIp = forms.CharField(required=True)
    process_info = forms.TextInput(required=True)
    note = forms.TextInput(required=True)
    physicalMachine = PhysicalMachine()
    phylist = physicalMachine.objects.all()
    phy = []
    for i in phylist:
        v = []
        v.append(i.physicalIp)
    phy.append(v)
    physicalIp = forms.ChoiceField(u"ip", choices=phy, required=True)


