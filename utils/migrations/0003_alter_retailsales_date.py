# Generated by Django 4.1.6 on 2023-02-13 12:45

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('utils', '0002_alter_retailsales_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='retailsales',
            name='date',
            field=models.DateField(default=django.utils.timezone.now),
        ),
    ]
