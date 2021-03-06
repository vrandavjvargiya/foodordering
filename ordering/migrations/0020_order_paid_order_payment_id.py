# Generated by Django 4.0.2 on 2022-03-25 07:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ordering', '0019_orderitem_remove_order_order_id_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='paid',
            field=models.BooleanField(default=False, null=True),
        ),
        migrations.AddField(
            model_name='order',
            name='payment_id',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
