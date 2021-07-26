# Generated by Django 3.2.5 on 2021-07-15 14:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0007_remove_comment_time'),
    ]

    operations = [
        migrations.AddField(
            model_name='listing',
            name='highest_bid',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='highest_bid', to='auctions.bid'),
        ),
        migrations.AddField(
            model_name='listing',
            name='status',
            field=models.BooleanField(default=True),
        ),
    ]
