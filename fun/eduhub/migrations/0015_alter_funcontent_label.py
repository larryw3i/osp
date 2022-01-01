# Generated by Django 3.2.7 on 2021-10-04 16:45

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('eduhub', '0014_auto_20211004_2129'),
    ]

    operations = [
        migrations.AlterField(
            model_name='funcontent',
            name='label',
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to='eduhub.label',
                verbose_name='Content label'),
        ),
    ]
