# Generated by Django 3.2.12 on 2022-06-11 13:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0031_auto_20220611_0950'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderitems',
            name='new_order',
            field=models.BooleanField(default=True),
        ),
    ]