# Generated by Django 4.0.2 on 2022-03-31 10:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ordering', '0024_order_razorpaypaymentid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderitem',
            name='item',
            field=models.CharField(max_length=1000),
        ),
    ]