# Generated by Django 3.2.10 on 2022-01-11 06:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0007_auto_20211226_1335'),
    ]

    operations = [
        migrations.AddField(
            model_name='dashboarduser',
            name='user_type',
            field=models.CharField(blank=True, default='sales', max_length=64, null=True),
        ),
    ]