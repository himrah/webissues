# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime
from django.conf import settings
import django.contrib.auth.models


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0006_require_contenttypes_0002'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='fullname',
            fields=[
                ('user_ptr', models.OneToOneField(auto_created=True, primary_key=True, parent_link=True, to=settings.AUTH_USER_MODEL, serialize=False)),
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
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=50)),
                ('created_date', models.DateTimeField(default=datetime.datetime.now, blank=True)),
                ('created_by', models.CharField(max_length=20)),
                ('status', models.CharField(default='----', choices=[('New', 'New'), ('In Process', 'In Process'), ('Complete', 'Complete')], max_length=10)),
                ('issue_description', models.TextField()),
                ('comments', models.TextField(blank=True)),
                ('modify_by', models.CharField(max_length=20)),
                ('priority', models.CharField(default='----', choices=[('High', 'High'), ('Low', 'Low'), ('Normal', 'Normal')], max_length=10)),
                ('tat', models.IntegerField()),
                ('assign', models.ForeignKey(to=settings.AUTH_USER_MODEL, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='project',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('name', models.CharField(max_length=20)),
                ('description', models.TextField()),
            ],
        ),
        migrations.AddField(
            model_name='issue',
            name='project_id',
            field=models.ForeignKey(to='track.project', null=True),
        ),
    ]
