# Generated by Django 4.2.2 on 2023-07-04 12:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0006_user_is_verified_user_otp'),
    ]

    operations = [
        migrations.AddField(
            model_name='menuitem',
            name='slug',
            field=models.SlugField(blank=True, null=True, unique=True),
        ),
    ]