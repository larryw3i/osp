# Generated by Django 4.0 on 2022-01-10 10:35

from django.db import migrations, models
import funuser.models


class Migration(migrations.Migration):

    dependencies = [
        ('funuser', '0003_auto_20211006_0116'),
    ]

    operations = [
        migrations.AlterField(
            model_name='funuser',
            name='avatar',
            field=models.ImageField(blank=True, upload_to=funuser.models.upload_to, verbose_name='Avatar'),
        ),
    ]