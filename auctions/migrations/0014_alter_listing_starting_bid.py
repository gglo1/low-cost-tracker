# Generated by Django 4.1.2 on 2023-12-10 21:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0013_user_profile_picture_alter_bid_amount'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listing',
            name='starting_bid',
            field=models.DecimalField(decimal_places=2, max_digits=10),
        ),
    ]
