# Generated by Django 4.1.2 on 2022-10-28 00:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('galleryapp', '0003_alter_album_title'),
    ]

    operations = [
        migrations.AddConstraint(
            model_name='photo',
            constraint=models.UniqueConstraint(fields=('title', 'album'), name='unique_title_album_combination'),
        ),
    ]
