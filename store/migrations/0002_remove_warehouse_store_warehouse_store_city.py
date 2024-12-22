# Generated by Django 5.1.4 on 2024-12-22 18:06

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='warehouse',
            name='store',
        ),
        migrations.AddField(
            model_name='warehouse',
            name='store_city',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='ware_house', to='store.storecity', verbose_name='Магазин'),
        ),
    ]