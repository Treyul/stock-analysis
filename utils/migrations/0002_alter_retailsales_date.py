# Generated by Django 4.1.6 on 2023-02-13 12:39

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('utils', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='retailsales',
            name='date',
            field=models.DateField(default=datetime.datetime(2023, 2, 13, 12, 39, 28, 910231, tzinfo=datetime.timezone.utc)),
        ),
    ]
