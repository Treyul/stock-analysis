# Generated by Django 4.1.6 on 2023-02-25 15:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('utils', '0007_alter_stock_depletion_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='ordered',
            name='arrived',
            field=models.BooleanField(default=False),
        ),
    ]