# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2016-12-26 10:37
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_category', '0005_test_timestamp'),
    ]

    operations = [
        migrations.AlterField(
            model_name='test',
            name='test_code',
            field=models.CharField(default='test_code', editable=False, max_length=255),
        ),
    ]