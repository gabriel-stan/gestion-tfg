# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('model', '0002_auto_20160307_2111'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tfg',
            name='conocimientos_previos',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='tfg',
            name='hard_soft',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
