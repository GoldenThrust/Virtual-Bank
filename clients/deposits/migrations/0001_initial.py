# Generated by Django 4.2.7 on 2023-12-19 13:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('transactions', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Deposit',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('transaction', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='deposit', to='transactions.transaction')),
            ],
        ),
    ]
