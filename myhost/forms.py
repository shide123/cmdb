# # -*- coding: utf-8 -*-
# from django import forms
# from myhost.models import *
# from myhost.models import VirtualMachine
#
#
# class PhysicalForm(forms.Form):
#     physicalIp = forms.CharField(required=True)
#     machineRoom_address = forms.CharField(required=True)
#     machineRoom_attr = forms.CharField(required=True)
#     machine_info = forms.CharField(required=True)
#     virtualMachine_ip = forms.CharField(required=False)
#     # selectphysicalMachine = PhysicalMachine.objects.filter(physicalIp=physicalIp)
#     # if selectphysicalMachine:
#     #     id = selectphysicalMachine.id
#     # virtualMachineModel = VirtualMachine.objects.filter(physicalMachine=selectphysicalMachine)
#     # virtualMachine_List = []
#     # for i in virtualMachineModel:
#     #     v = []
#     #     v.append(i.virtualIp)
#     #     virtualMachine_List.append(v)
#     # virtualMachine_ip = forms.MultipleChoiceField(choices=virtualMachine_List, widget=forms.CheckboxSelectMultiple(),
#     #                                               required=False)
#
#
# class VirtualForm(forms.Form):
#     virtualIp = forms.CharField(required=True)
#     physicalMachine = PhysicalMachine.objects.all()
#     physicalip_list = []
#     for phyobj in physicalMachine:
#         p = []
#         p.append(phyobj)
#         physicalip_list.append(p)
#     physicalIp = forms.CharField(widget=forms.widgets.Select(choices=physicalip_list),
#                                  required=False)
#     note = forms.CharField(required=True)
#     process_info = forms.CharField(required=True)
