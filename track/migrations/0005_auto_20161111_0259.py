# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('track', '0004_auto_20161111_0255'),
    ]

    operations = [
        migrations.AlterField(
            model_name='issue',
            name='comments',
            field=models.TextField(blank=True),
        ),
    ]
