# Generated by Django 4.0.4 on 2022-06-01 14:40

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='LocationModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('lat', models.DecimalField(blank=True, decimal_places=20, max_digits=30, null=True)),
                ('lng', models.DecimalField(blank=True, decimal_places=20, max_digits=30, null=True)),
                ('primary_text', models.TextField(blank=True, max_length=100, null=True)),
                ('secondary_text', models.TextField(blank=True, max_length=100, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Booking',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pickup_date', models.DateField(null=True)),
                ('pickup_time', models.TimeField(null=True)),
                ('additional_helpers', models.IntegerField(blank=True, default=0, null=True)),
                ('carry_floor', models.IntegerField(blank=True, default=0, null=True)),
                ('vehicle_type', models.FloatField(blank=True, default=1.0, null=True)),
                ('payment_option', models.CharField(blank=True, default='CASH', max_length=50, null=True)),
                ('drivers_note', models.TextField(blank=True, default='No note left', max_length=1000, null=True)),
                ('driver_rating', models.IntegerField(blank=True, default=0)),
                ('quote_price', models.FloatField(blank=True, default=1.0, null=True)),
                ('distance_km', models.FloatField(blank=True, default=0.0, null=True)),
                ('booking_completed', models.BooleanField(default=False)),
                ('booking_cancelled', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('assigned_driver', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
                ('booker', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='booker', to=settings.AUTH_USER_MODEL)),
                ('routes', models.ManyToManyField(blank=True, to='booking.locationmodel')),
            ],
        ),
    ]
