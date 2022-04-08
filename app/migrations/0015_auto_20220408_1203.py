# Generated by Django 3.2.12 on 2022-04-08 12:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0014_auto_20220405_2029'),
    ]

    operations = [
        migrations.AddField(
            model_name='services',
            name='comm_status',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='services',
            name='commission',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.CreateModel(
            name='SalesBonus',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.FloatField(blank=True, null=True)),
                ('detail', models.CharField(blank=True, max_length=512, null=True)),
                ('date', models.DateField(blank=True, null=True)),
                ('created_at', models.DateField(auto_now_add=True, null=True)),
                ('emp', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.dashboarduser')),
            ],
        ),
    ]
