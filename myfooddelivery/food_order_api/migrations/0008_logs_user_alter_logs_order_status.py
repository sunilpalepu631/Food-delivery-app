# Generated by Django 5.0.1 on 2024-01-30 04:22

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('food_order_api', '0007_order_payment_date_order_payment_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='logs',
            name='user',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='food_order_api.user'),
        ),
        migrations.AlterField(
            model_name='logs',
            name='order_status',
            field=models.CharField(choices=[('PENDING', 'Pending'), ('PAYMENT_DONE', 'Payment Done'), ('DISPATCHED', 'Dispatched'), ('DELIVERED', 'Delivered')], max_length=50),
        ),
    ]
