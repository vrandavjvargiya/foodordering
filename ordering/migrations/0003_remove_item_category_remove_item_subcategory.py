# Generated by Django 4.0.2 on 2022-03-07 11:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ordering', '0002_item_category_item_image_item_subcategory_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='item',
            name='category',
        ),
        migrations.RemoveField(
            model_name='item',
            name='subcategory',
        ),
    ]
