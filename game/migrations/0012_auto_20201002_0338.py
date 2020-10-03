# Generated by Django 3.1.2 on 2020-10-02 03:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0011_auto_20201002_0314'),
    ]

    operations = [
        migrations.AlterField(
            model_name='game',
            name='game_name',
            field=models.CharField(default='Bananagrams', max_length=30),
        ),
        migrations.AlterField(
            model_name='game',
            name='remaining_tiles',
            field=models.CharField(default='TIUIJYEYDREARLVKDFEWOEDEFBAPTIMLNIUSERTNIEXNZIGAEMGLERZHUTIESAVOAPXSLUORBOEOUQOGNRKYOAIAOTECREHSBMADAEIWEEEQSOACSOICTNANTRWENTJVDRIOPAINLUTAGFDH', max_length=144),
        ),
        migrations.AlterField(
            model_name='game',
            name='url_key',
            field=models.CharField(default='Z3WOtGDKdp0u78sSCHdL', max_length=20),
        ),
    ]
