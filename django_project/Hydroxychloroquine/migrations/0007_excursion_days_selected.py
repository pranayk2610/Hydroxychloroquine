# Generated by Django 3.1.2 on 2020-11-25 00:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Hydroxychloroquine', '0006_auto_20201109_2345'),
    ]

    operations = [
        migrations.AddField(
            model_name='excursion',
            name='days_selected',
            field=models.CharField(default='1', max_length=128),
        ),
    ]
