# Generated by Django 4.0.2 on 2022-03-11 09:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ordering', '0005_item_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='image',
            field=models.ImageField(upload_to=''),
        ),
    ]
