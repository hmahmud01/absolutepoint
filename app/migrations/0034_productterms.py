# Generated by Django 3.2.12 on 2022-06-11 17:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0033_auto_20220611_1354'),
    ]

    operations = [
        migrations.CreateModel(
            name='productTerms',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('terms', models.CharField(blank=True, max_length=512, null=True)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.serviceproduct')),
            ],
        ),
    ]