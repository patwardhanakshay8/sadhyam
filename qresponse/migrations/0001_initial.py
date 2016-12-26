# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2016-12-23 14:32
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('quiz', '0003_auto_20161222_0933'),
        ('user_category', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Response',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('response', models.CharField(default='response', max_length=255)),
                ('correct', models.BooleanField(default=False)),
                ('marks_obtained', models.FloatField(default=0.0)),
                ('time_taken', models.FloatField(default=0.0)),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='quiz.Question')),
                ('subscriber', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user_category.Subscriber')),
                ('test', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user_category.Test')),
                ('test_template', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='quiz.TestTemplate')),
            ],
        ),
    ]