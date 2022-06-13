# Generated by Django 3.2.12 on 2022-06-06 16:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0028_ticket'),
    ]

    operations = [
        migrations.CreateModel(
            name='AppUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fname', models.CharField(blank=True, max_length=128, null=True)),
                ('lname', models.CharField(blank=True, max_length=128, null=True)),
                ('telid', models.CharField(blank=True, max_length=128, null=True)),
                ('email', models.CharField(blank=True, max_length=64, null=True)),
                ('address', models.CharField(blank=True, max_length=256, null=True)),
                ('country', models.CharField(blank=True, max_length=32, null=True)),
                ('state', models.CharField(blank=True, max_length=32, null=True)),
                ('zipcode', models.CharField(blank=True, max_length=32, null=True)),
            ],
        ),
    ]