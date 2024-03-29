# Generated by Django 5.0 on 2024-01-23 19:12

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Locations',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=255)),
                ('latitude', models.DecimalField(decimal_places=20, max_digits=30)),
                ('longitude', models.DecimalField(decimal_places=20, max_digits=30)),
                ('user_id', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='locations', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Локации',
                'verbose_name_plural': 'Локации',
                'ordering': ['name'],
                'indexes': [models.Index(fields=['name'], name='weather_loc_name_2a97bb_idx')],
                'unique_together': {('name', 'latitude', 'longitude', 'user_id')},
            },
        ),
    ]
