# Generated by Django 4.0.2 on 2022-03-31 07:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ordering', '0022_order_address_orderitem_address_alter_order_amount_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='address',
        ),
        migrations.RemoveField(
            model_name='orderitem',
            name='address',
        ),
    ]
