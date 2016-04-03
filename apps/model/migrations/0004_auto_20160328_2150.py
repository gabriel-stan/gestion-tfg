# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('model', '0003_auto_20160307_2117'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='alumno',
            options={'permissions': (('login', 'Puede loguearse'),)},
        ),
        migrations.AlterModelOptions(
            name='profesor',
            options={'permissions': (('crear_tfg', 'Puede crear tfgs'),)},
        ),
    ]
