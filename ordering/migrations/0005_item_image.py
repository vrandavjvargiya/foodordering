# Generated by Django 4.0.2 on 2022-03-08 12:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ordering', '0004_remove_item_image_alter_item_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='image',
            field=models.ImageField(default='', upload_to='ordering/images'),
        ),
    ]