# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import django.contrib.auth.models
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0006_require_contenttypes_0002'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='fullname',
            fields=[
                ('user_ptr', models.OneToOneField(auto_created=True, to=settings.AUTH_USER_MODEL, serialize=False, primary_key=True, parent_link=True)),
            ],
            options={
                'abstract': False,
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
            },
            bases=('auth.user',),
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='issue',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=50)),
                ('created_date', models.DateTimeField(blank=True, default=datetime.datetime.now)),
                ('created_by', models.CharField(max_length=20, blank=True)),
                ('status', models.CharField(max_length=10, blank=True, default='----', choices=[('New', 'New'), ('In Process', 'In Process'), ('Complete', 'Complete')])),
                ('comment', models.TextField(blank=True)),
                ('modify_by', models.CharField(max_length=20, blank=True)),
                ('priority', models.IntegerField(null=True)),
                ('tat', models.IntegerField(null=True)),
                ('assign', models.ForeignKey(null=True, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
