# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-11-16 07:28
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myhost', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='physicalmachine',
            name='machine_info',
        ),
        migrations.RemoveField(
            model_name='virtualmachine',
            name='physicalMachine',
        ),
        migrations.DeleteModel(
            name='PhysicalMachine',
        ),
        migrations.DeleteModel(
            name='VirtualMachine',
        ),
    ]
