# Generated by Django 3.2.12 on 2022-04-25 17:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0016_services_comm_amount'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='serviceproduct',
            name='measurement',
        ),
        migrations.RemoveField(
            model_name='serviceproduct',
            name='price',
        ),
        migrations.CreateModel(
            name='variableProductPrice',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('measurement', models.IntegerField(blank=True, null=True)),
                ('price', models.FloatField(blank=True, null=True)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.serviceproduct')),
            ],
        ),
    ]
