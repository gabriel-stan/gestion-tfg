# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('model', '0004_auto_20160328_2150'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='profesor',
            options={'permissions': (('add_tfg', 'Puede crear tfgs'),)},
        ),
    ]
