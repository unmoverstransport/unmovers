# Generated by Django 4.0.4 on 2022-06-02 09:46

from django.db import migrations, models
import gallary.models


class Migration(migrations.Migration):

    dependencies = [
        ('gallary', '0002_alter_itemgallarymodel_image_gallary'),
    ]

    operations = [
        migrations.AlterField(
            model_name='itemgallarymodel',
            name='image_gallary',
            field=models.ImageField(upload_to=gallary.models.upload_to_gallary),
        ),
    ]
