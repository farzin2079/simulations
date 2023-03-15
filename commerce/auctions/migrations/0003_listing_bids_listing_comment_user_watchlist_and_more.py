# Generated by Django 4.1.2 on 2023-03-14 09:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0002_alter_bids_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='listing',
            name='bids',
            field=models.ForeignKey(blank=True, default=1, on_delete=django.db.models.deletion.PROTECT, to='auctions.bids'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='listing',
            name='comment',
            field=models.ManyToManyField(blank=True, to='auctions.comment'),
        ),
        migrations.AddField(
            model_name='user',
            name='watchlist',
            field=models.ManyToManyField(to='auctions.listing'),
        ),
        migrations.DeleteModel(
            name='Watchlist',
        ),
    ]
