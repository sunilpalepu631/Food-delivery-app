# Generated by Django 5.0.1 on 2024-01-09 07:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('food_order_api', '0002_order_items_alter_order_delivery_person_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='items',
            field=models.JSONField(),
        ),
    ]
