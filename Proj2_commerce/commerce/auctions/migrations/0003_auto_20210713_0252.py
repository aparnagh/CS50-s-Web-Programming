# Generated by Django 3.2.5 on 2021-07-13 06:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0002_bid_comment_listing_watchlist'),
    ]

    operations = [
        migrations.RenameField(
            model_name='comment',
            old_name='comment_title',
            new_name='title',
        ),
        migrations.RemoveField(
            model_name='listing',
            name='bid',
        ),
        migrations.AddField(
            model_name='bid',
            name='listing',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, related_name='bids', to='auctions.listing'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='listing',
            name='price',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=9),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='listing',
            name='category',
            field=models.CharField(blank=True, max_length=64, null=True),
        ),
        migrations.AlterField(
            model_name='listing',
            name='photo',
            field=models.CharField(blank=True, max_length=2048, null=True),
        ),
    ]
