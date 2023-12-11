# Generated by Django 4.1.2 on 2023-12-10 11:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0012_alter_category_options_category_image_listing_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='profile_picture',
            field=models.ImageField(blank=True, null=True, upload_to='images/profiles'),
        ),
        migrations.AlterField(
            model_name='bid',
            name='amount',
            field=models.DecimalField(decimal_places=2, max_digits=10),
        ),
    ]
