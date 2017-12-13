# -*- coding: utf-8 -*-
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, render_to_response, get_object_or_404
from django.template import RequestContext
from myhost.forms import IdcForm
from myhost.models import IDC, Project


def my_render(template, data, request):
    return render_to_response(template, data, context_instance=RequestContext(request))


def idc_add(request):
    """add idc"""
    if request.method == 'POST':
        idc = IdcForm(request.POST)
        if idc.is_valid():
            idc_name = idc.request.POST.get("name")
            if IDC.objects.filter(name=idc_name):
                emg = u'添加失败, 此IDC %s 已存在!' % idc_name
                return render(request, 'myhost:idc_add', {'emg', emg})
            idc.save()
            return HttpResponseRedirect("myhost:idc_list")
    else:
        idc = IdcForm()
    return render_to_response('myhost:idc_add', locals(), context_instance=RequestContext(request))


def idc_edit(request):
    """edit idc"""
    uuid = request.GET.get('uuid', '')
    idc = get_object_or_404(IDC, uuid=uuid)
    if request.method == 'POST':
        uf = IdcForm(request.POST, instance=idc)
        if uf.is_valid():
            uf.save()
            return HttpResponseRedirect("myhost:idc_list")
    else:
        uf = IdcForm(instance=idc)
        return my_render('myhost:idc_update', locals(), request)


def idc_list(request):
    """list idc"""
    idcs = IDC.objects.all()
    server_type = Project.objects.all()
    return render(request, 'idc_list.html', {'idcs': idcs, 'server_type': server_type})


def idc_detail(request):
    """idc detail"""
    uuid = request.GET.get('uuid', '')
    idc = get_object_or_404(IDC, uuid=uuid)
    return render(request, 'idc_detail.html', {'idc': idc})


def idc_delete(request):
    """idc delete"""
    uuid = request.GET.get('uuid', '')
    idc = get_object_or_404(IDC, uuid=uuid)
    idc_name = idc.name
    idc.delete()
    return HttpResponseRedirect('myhost:idc')
