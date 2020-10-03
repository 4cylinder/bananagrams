# Generated by Django 3.1.2 on 2020-10-02 04:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0012_auto_20201002_0338'),
    ]

    operations = [
        migrations.AlterField(
            model_name='game',
            name='end_time',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='game',
            name='remaining_tiles',
            field=models.CharField(default='GAMRCILIQSIENROLYAOOIWSOFREEAUTDRCNIBMFASRUYATABVDUIQODAGESHOLRWMUILXTPXSTPAONDNAVEYPHJERAKIIOTJTNIGERNNOODIZIDSETHUEGNETEAOZEBRCELEEKAUFEETEWAV', max_length=144),
        ),
        migrations.AlterField(
            model_name='game',
            name='url_key',
            field=models.CharField(default='GOaZKGU3OTboqlCRac2a', max_length=20),
        ),
    ]
