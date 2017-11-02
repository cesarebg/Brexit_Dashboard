# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-10-09 15:11
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Inflation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pub_data', models.DateTimeField(verbose_name='Year')),
                ('inflation_value', models.IntegerField(default=0)),
            ],
        ),
    ]