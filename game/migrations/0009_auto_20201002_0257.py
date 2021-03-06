# Generated by Django 3.1.2 on 2020-10-02 02:57

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0008_auto_20201002_0250'),
    ]

    operations = [
        migrations.RenameField(
            model_name='event',
            old_name='info',
            new_name='event_info',
        ),
        migrations.AddField(
            model_name='event',
            name='event_time',
            field=models.TimeField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='game',
            name='remaining_tiles',
            field=models.CharField(default='UMEINEXSDECOSARYFREQWLROMYTXADDNOAOPATQARIOWEDJINIAVLGZOBYCZEETELDAOPWUFRBAIRALNIHETEUTHOEIEONNITGBDHFTEIEISANARUSTVEERNAOGKLKOVAEJGEUTISPCRUSMI', max_length=144),
        ),
        migrations.AlterField(
            model_name='game',
            name='url_key',
            field=models.CharField(default='M0Ol5tDjklFHgJ4ZSb1L', max_length=20),
        ),
    ]
