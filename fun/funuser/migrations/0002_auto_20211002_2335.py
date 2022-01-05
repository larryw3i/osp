# Generated by Django 3.2.7 on 2021-10-02 15:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('funuser', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='funuser',
            name='is_address_outward',
            field=models.BooleanField(default=False, verbose_name='Is outward ?'),
        ),
        migrations.AlterField(
            model_name='funuser',
            name='is_birth_date_outward',
            field=models.BooleanField(default=False, verbose_name='Is outward ?'),
        ),
        migrations.AlterField(
            model_name='funuser',
            name='is_college_outward',
            field=models.BooleanField(default=False, verbose_name='Is outward ?'),
        ),
        migrations.AlterField(
            model_name='funuser',
            name='is_hobby_outward',
            field=models.BooleanField(default=False, verbose_name='Is outward ?'),
        ),
        migrations.AlterField(
            model_name='funuser',
            name='is_hometown_outward',
            field=models.BooleanField(default=False, verbose_name='Is outward ?'),
        ),
        migrations.AlterField(
            model_name='funuser',
            name='is_motto_outward',
            field=models.BooleanField(default=False, verbose_name='Is outward ?'),
        ),
        migrations.AlterField(
            model_name='funuser',
            name='is_occupation_outward',
            field=models.BooleanField(default=False, verbose_name='Is outward ?'),
        ),
    ]