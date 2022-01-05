# Generated by Django 3.2.7 on 2021-10-02 15:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('funhome', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='funhomesticker',
            options={
                'verbose_name': 'Home sticker(NEW)',
                'verbose_name_plural': 'Home stickers(NEW)'},
        ),
        migrations.AlterField(
            model_name='funhomesticker',
            name='is_hidden',
            field=models.BooleanField(
                default=False,
                verbose_name='Hidden ?'),
        ),
        migrations.AlterField(
            model_name='homesticker',
            name='is_hidden',
            field=models.BooleanField(
                default=False,
                verbose_name='Hidden ?'),
        ),
    ]