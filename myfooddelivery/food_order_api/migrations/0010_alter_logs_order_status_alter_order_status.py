# Generated by Django 5.0.1 on 2024-01-31 02:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('food_order_api', '0009_alter_logs_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='logs',
            name='order_status',
            field=models.CharField(choices=[('PAYMENT_PENDING', 'Payment Pending'), ('PAYMENT_DONE', 'Payment Done'), ('ACCEPTED', 'Accepted'), ('CANCELLED', 'Cancelled'), ('DISPATCHED', 'Dispatched'), ('DELIVERED', 'Delivered')], max_length=50),
        ),
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('PAYMENT_PENDING', 'Payment Pending'), ('PAYMENT_DONE', 'Payment Done'), ('ACCEPTED', 'Accepted'), ('CANCELLED', 'Cancelled'), ('DISPATCHED', 'Dispatched'), ('DELIVERED', 'Delivered')], default='PAYMENT_PENDING', max_length=50),
        ),
    ]
