# Generated by Django 4.2.1 on 2023-06-12 16:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('watchlist_app', '0005_watchlist_avg_rating_watchlist_number_rating'),
    ]

    operations = [
        migrations.RenameField(
            model_name='watchlist',
            old_name='created_at',
            new_name='created',
        ),
    ]
