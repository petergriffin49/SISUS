# Generated by Django 5.1.1 on 2024-12-03 23:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0004_item_edit'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item_edit',
            name='time',
            field=models.DateField(),
        ),
    ]