# Generated by Django 4.2.6 on 2023-11-20 02:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_watchlist_name_alter_watchlist_cryptocurrencies'),
    ]

    operations = [
        migrations.AlterField(
            model_name='watchlist',
            name='cryptocurrencies',
            field=models.ManyToManyField(null=True, to='core.cryptocurrency'),
        ),
    ]
