# Generated by Django 3.1.2 on 2020-10-01 22:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0003_auto_20201001_2237'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='player',
            name='display_name',
        ),
        migrations.AlterField(
            model_name='game',
            name='url_key',
            field=models.CharField(default='tssYLleim5aQ05KWenfa', max_length=20),
        ),
    ]
