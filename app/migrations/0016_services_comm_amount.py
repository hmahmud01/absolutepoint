# Generated by Django 3.2.12 on 2022-04-08 12:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0015_auto_20220408_1203'),
    ]

    operations = [
        migrations.AddField(
            model_name='services',
            name='comm_amount',
            field=models.FloatField(blank=True, null=True),
        ),
    ]