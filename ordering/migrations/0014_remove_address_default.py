# Generated by Django 4.0.2 on 2022-03-24 11:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ordering', '0013_remove_order_items_orderline'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='address',
            name='default',
        ),
    ]
