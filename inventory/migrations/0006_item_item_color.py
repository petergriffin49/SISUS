# Generated by Django 5.1.1 on 2024-12-07 18:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0005_alter_item_edit_time'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='Item_color',
            field=models.CharField(default='#000000', max_length=7),
        ),
    ]