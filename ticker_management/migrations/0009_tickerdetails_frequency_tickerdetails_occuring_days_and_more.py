# Generated by Django 4.0.5 on 2022-07-04 07:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ticker_management', '0008_remove_tickerdetails_reason_for_delete_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='tickerdetails',
            name='frequency',
            field=models.CharField(max_length=30, null=True),
        ),
        migrations.AddField(
            model_name='tickerdetails',
            name='occuring_days',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='tickerhistory',
            name='frequency',
            field=models.CharField(max_length=30, null=True),
        ),
        migrations.AddField(
            model_name='tickerhistory',
            name='occuring_days',
            field=models.CharField(max_length=50, null=True),
        ),
    ]
