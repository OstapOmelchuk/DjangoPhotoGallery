# Generated by Django 4.1.2 on 2022-10-28 14:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('galleryapp', '0005_remove_photo_unique_title_album_combination_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='photo',
            name='title',
            field=models.CharField(max_length=100),
        ),
    ]