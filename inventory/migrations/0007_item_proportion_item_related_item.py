# Generated by Django 5.1.1 on 2024-12-08 19:15

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0006_item_item_color'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='Proportion',
            field=models.FloatField(default=1),
        ),
        migrations.AddField(
            model_name='item',
            name='Related_item',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='related_item', to='inventory.item'),
        ),
    ]
