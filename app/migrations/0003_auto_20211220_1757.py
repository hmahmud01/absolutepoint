# Generated by Django 3.2.10 on 2021-12-20 17:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_auto_20211220_1745'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notices',
            name='validity',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='services',
            name='counter',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='services',
            name='price',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='userrank',
            name='tier',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
    ]
