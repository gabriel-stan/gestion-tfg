# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('model', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tfg',
            name='cotutor',
            field=models.ForeignKey(related_name='cotutor', default=None, to='model.Profesor', null=True),
        ),
    ]
