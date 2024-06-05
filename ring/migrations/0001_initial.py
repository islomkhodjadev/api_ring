# Generated by Django 5.0.4 on 2024-05-01 11:45

import django.db.models.deletion
import ring.models
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('founder', models.CharField(max_length=200)),
                ('phoneNumber', models.CharField(max_length=13, validators=[ring.models.validate_uzbek_phone_number])),
                ('companyName', models.CharField(max_length=200, unique=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Assistant',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField()),
                ('name', models.CharField(max_length=200, unique=True)),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ring.company')),
            ],
        ),
    ]