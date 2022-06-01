# Generated by Django 4.0.4 on 2022-06-01 14:40

from django.db import migrations, models
import gallary.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ItemGallaryModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image_gallary', models.ImageField(upload_to=gallary.models.upload_to_gallary, verbose_name='image_gallary')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]
