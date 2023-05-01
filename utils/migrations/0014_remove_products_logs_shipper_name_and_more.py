# Generated by Django 4.1.6 on 2023-04-15 14:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('utils', '0013_alter_products_order_logs_order_price'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='products_logs',
            name='shipper_name',
        ),
        migrations.AlterField(
            model_name='products_logs',
            name='order_id',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='utils.products_order_logs'),
        ),
    ]