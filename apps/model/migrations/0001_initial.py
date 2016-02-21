# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.contrib.auth.models
import django.utils.timezone
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0006_require_contenttypes_0002'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comision_Evaluacion',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
            ],
        ),
        migrations.CreateModel(
            name='Evaluacion_Tfg_Tutor',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('departamento', models.CharField(max_length=100)),
                ('fecha', models.DateField()),
                ('calificacion', models.FloatField()),
                ('sub_cal_1', models.FloatField()),
                ('sub_cal_2', models.FloatField()),
                ('sub_cal_3', models.FloatField()),
                ('sub_cal_4', models.FloatField()),
                ('sub_cal_5', models.FloatField()),
                ('sub_cal_6', models.FloatField()),
                ('sub_cal_7', models.FloatField()),
                ('sub_cal_8', models.FloatField()),
                ('observaciones', models.CharField(max_length=500, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Tfg',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('tipo', models.CharField(max_length=100)),
                ('titulo', models.CharField(max_length=100)),
                ('n_alumnos', models.IntegerField()),
                ('descripcion', models.TextField()),
                ('conocimientos_previos', models.CharField(max_length=100)),
                ('hard_soft', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Tfg_Asig',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('tfg', models.ForeignKey(default=None, to='model.Tfg')),
            ],
        ),
        migrations.CreateModel(
            name='Tribunales',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('fecha', models.DateField()),
                ('hora', models.DateTimeField()),
                ('observaciones', models.CharField(max_length=500, null=True)),
                ('comision', models.ForeignKey(default=None, to='model.Comision_Evaluacion')),
                ('tfg', models.ForeignKey(default=None, to='model.Tfg_Asig')),
            ],
        ),
        migrations.CreateModel(
            name='Usuario',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(null=True, verbose_name='last login', blank=True)),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, max_length=30, validators=[django.core.validators.RegexValidator('^[\\w.@+-]+$', 'Enter a valid username. This value may contain only letters, numbers and @/./+/-/_ characters.', 'invalid')], help_text='Required. 30 characters or fewer. Letters, digits and @/./+/-/_ only.', unique=True, verbose_name='username')),
                ('first_name', models.CharField(max_length=30, verbose_name='first name', blank=True)),
                ('last_name', models.CharField(max_length=30, verbose_name='last name', blank=True)),
                ('email', models.EmailField(max_length=254, verbose_name='email address', blank=True)),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
            ],
            options={
                'abstract': False,
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Administrador',
            fields=[
                ('usuario_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='model.Usuario')),
            ],
            options={
                'abstract': False,
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
            },
            bases=('model.usuario',),
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Alumno',
            fields=[
                ('usuario_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='model.Usuario')),
            ],
            options={
                'abstract': False,
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
            },
            bases=('model.usuario',),
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Profesor',
            fields=[
                ('usuario_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='model.Usuario')),
                ('departamento', models.CharField(max_length=100)),
            ],
            options={
                'abstract': False,
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
            },
            bases=('model.usuario',),
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.AddField(
            model_name='usuario',
            name='groups',
            field=models.ManyToManyField(related_query_name='user', related_name='user_set', to='auth.Group', blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', verbose_name='groups'),
        ),
        migrations.AddField(
            model_name='usuario',
            name='user_permissions',
            field=models.ManyToManyField(related_query_name='user', related_name='user_set', to='auth.Permission', blank=True, help_text='Specific permissions for this user.', verbose_name='user permissions'),
        ),
        migrations.AddField(
            model_name='evaluacion_tfg_tutor',
            name='tfg',
            field=models.ForeignKey(default=None, to='model.Tfg_Asig'),
        ),
        migrations.AddField(
            model_name='tfg_asig',
            name='alumno_1',
            field=models.ForeignKey(related_name='alumno_1', default=None, to='model.Alumno'),
        ),
        migrations.AddField(
            model_name='tfg_asig',
            name='alumno_2',
            field=models.ForeignKey(related_name='alumno_2', default=None, to='model.Alumno', null=True),
        ),
        migrations.AddField(
            model_name='tfg_asig',
            name='alumno_3',
            field=models.ForeignKey(related_name='alumno_3', default=None, to='model.Alumno', null=True),
        ),
        migrations.AddField(
            model_name='tfg',
            name='cotutor',
            field=models.ForeignKey(related_name='cotutor', default=None, to='model.Profesor'),
        ),
        migrations.AddField(
            model_name='tfg',
            name='tutor',
            field=models.ForeignKey(related_name='tutor', default=None, to='model.Profesor'),
        ),
        migrations.AddField(
            model_name='evaluacion_tfg_tutor',
            name='tutor',
            field=models.ForeignKey(related_name='tutor_tfg', default=None, to='model.Profesor'),
        ),
        migrations.AddField(
            model_name='comision_evaluacion',
            name='presidente',
            field=models.ForeignKey(related_name='presidente', default=None, to='model.Profesor'),
        ),
        migrations.AddField(
            model_name='comision_evaluacion',
            name='sup_presidente',
            field=models.ForeignKey(related_name='sup_presidente', default=None, to='model.Profesor'),
        ),
        migrations.AddField(
            model_name='comision_evaluacion',
            name='sup_titular_1',
            field=models.ForeignKey(related_name='sup_titular_1', default=None, to='model.Profesor'),
        ),
        migrations.AddField(
            model_name='comision_evaluacion',
            name='sup_titular_2',
            field=models.ForeignKey(related_name='sup_titular_2', default=None, to='model.Profesor', null=True),
        ),
        migrations.AddField(
            model_name='comision_evaluacion',
            name='titular_1',
            field=models.ForeignKey(related_name='titular_1', default=None, to='model.Profesor'),
        ),
        migrations.AddField(
            model_name='comision_evaluacion',
            name='titular_2',
            field=models.ForeignKey(related_name='titular_2', default=None, to='model.Profesor', null=True),
        ),
    ]
