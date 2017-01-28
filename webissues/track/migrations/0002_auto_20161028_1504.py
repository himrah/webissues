# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('track', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='project',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
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
