# Generated by Django 5.1.1 on 2024-12-08 20:01

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0008_alter_item_item_amount_alter_item_item_lowstock_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='Related_item',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='inventory.item'),
        ),
    ]