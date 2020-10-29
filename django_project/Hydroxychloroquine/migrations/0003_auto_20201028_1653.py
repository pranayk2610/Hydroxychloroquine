# Generated by Django 3.1.2 on 2020-10-28 20:53

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Hydroxychloroquine', '0002_report'),
    ]

    operations = [
        migrations.CreateModel(
            name='Building',
            fields=[
                ('building_id', models.IntegerField(primary_key=True, serialize=False)),
                ('building_name', models.CharField(max_length=128)),
            ],
        ),
        migrations.AlterField(
            model_name='report',
            name='date_last_on_campus',
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name='report',
            name='date_of_test',
            field=models.DateTimeField(),
        ),
        migrations.CreateModel(
            name='Excursion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_time', models.DateTimeField()),
                ('end_time', models.DateTimeField()),
                ('building_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Hydroxychloroquine.building')),
                ('report_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Hydroxychloroquine.report')),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]