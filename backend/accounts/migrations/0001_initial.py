# Generated by Django 4.2.7 on 2023-11-25 18:42

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('account_type', models.CharField(choices=[('SAVINGS', 'Savings'), ('CURRENT', 'Current')], default='SAVINGS', max_length=20)),
                ('balance', models.DecimalField(decimal_places=2, default=0, max_digits=15)),
                ('number', models.BigIntegerField(unique=True)),
                ('currency', models.CharField(choices=[('USD', 'USD'), ('EUR', 'EUR'), ('GBP', 'GBP'), ('NGN', 'NGN')], max_length=3)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
