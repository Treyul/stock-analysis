# Generated by Django 4.1.6 on 2023-03-07 16:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='users',
            name='rights',
            field=models.BooleanField(),
        ),
    ]
