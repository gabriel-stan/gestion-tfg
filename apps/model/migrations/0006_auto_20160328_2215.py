# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('model', '0005_auto_20160328_2206'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='alumno',
            options={'verbose_name': 'user', 'verbose_name_plural': 'users'},
        ),
        migrations.AlterModelOptions(
            name='profesor',
            options={'verbose_name': 'user', 'verbose_name_plural': 'users'},
        ),
    ]
