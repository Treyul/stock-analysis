# Generated by Django 4.1.6 on 2023-05-06 17:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('utils', '0020_alter_products_available_batch_no_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Credit_and_Debit_Management',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Shop_name', models.CharField(max_length=50)),
                ('debt', models.IntegerField()),
                ('Amount_paid', models.IntegerField()),
            ],
        ),
        migrations.DeleteModel(
            name='AvailableStock',
        ),
        migrations.DeleteModel(
            name='LocalSales',
        ),
        migrations.DeleteModel(
            name='Ordered',
        ),
        migrations.DeleteModel(
            name='RetailSales',
        ),
        migrations.DeleteModel(
            name='Stock',
        ),
    ]
