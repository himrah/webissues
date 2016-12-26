# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('track', '0003_issue_comments'),
    ]

    operations = [
        migrations.AlterField(
            model_name='issue',
            name='comments',
            field=models.TextField(),
        ),
    ]
