# Generated by Django 4.2.2 on 2023-07-10 16:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0008_remove_menuitem_slug'),
    ]

    operations = [
        migrations.CreateModel(
            name='AddCartItem',
            fields=[
                ('cart_no', models.AutoField(primary_key=True, serialize=False)),
                ('qty', models.IntegerField(blank=True, default=0, null=True)),
            ],
        ),
    ]