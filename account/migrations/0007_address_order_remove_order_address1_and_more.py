# Generated by Django 4.2.2 on 2023-07-31 14:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0006_payment'),
    ]

    operations = [
        migrations.CreateModel(
            name='Address_Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address1', models.CharField(max_length=350)),
                ('address2', models.CharField(max_length=350)),
                ('city', models.CharField(max_length=100)),
                ('phone', models.PositiveBigIntegerField()),
                ('post_code', models.BigIntegerField()),
            ],
        ),
        migrations.RemoveField(
            model_name='order',
            name='address1',
        ),
        migrations.RemoveField(
            model_name='order',
            name='address2',
        ),
        migrations.RemoveField(
            model_name='order',
            name='city',
        ),
        migrations.RemoveField(
            model_name='order',
            name='phone',
        ),
        migrations.RemoveField(
            model_name='order',
            name='post_code',
        ),
    ]
