# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2016-12-24 12:57
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user_category', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='exam',
            old_name='exam',
            new_name='exam_subscribed',
        ),
    ]