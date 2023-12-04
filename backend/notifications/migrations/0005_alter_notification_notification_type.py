# Generated by Django 4.2.7 on 2023-11-28 15:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notifications', '0004_alter_notification_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notification',
            name='notification_type',
            field=models.CharField(choices=[('USER_NOTIFICATION', 'User Notification'), ('TRANSACTION_NOTIFICATION', 'Transaction Alert'), ('ACCOUNT_NOTIFICATION', 'Account Alert'), ('SECURITY_NOTIFICATION', 'Security Notification')], max_length=30),
        ),
    ]