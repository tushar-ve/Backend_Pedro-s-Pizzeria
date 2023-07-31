# Generated by Django 4.2.2 on 2023-07-31 14:43

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0008_delete_address_order'),
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
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
