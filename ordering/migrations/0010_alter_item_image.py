# Generated by Django 4.0.2 on 2022-03-14 08:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ordering', '0009_alter_item_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='image',
            field=models.ImageField(default='', upload_to='ordering/static/image/'),
        ),
    ]
