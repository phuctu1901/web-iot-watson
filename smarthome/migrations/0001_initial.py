# Generated by Django 2.2.5 on 2019-10-11 02:51

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Scheduler',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('device', models.CharField(max_length=120, verbose_name='Device')),
                ('status', models.IntegerField(verbose_name='Status')),
                ('event', models.CharField(max_length=120, verbose_name='Event')),
                ('time', models.CharField(max_length=60, verbose_name='Time')),
            ],
        ),
    ]
