# Generated by Django 3.2.10 on 2022-03-08 16:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0010_client_productcategory_serviceorder_serviceproduct'),
    ]

    operations = [
        migrations.AddField(
            model_name='services',
            name='date',
            field=models.DateField(blank=True, null=True),
        ),
    ]
