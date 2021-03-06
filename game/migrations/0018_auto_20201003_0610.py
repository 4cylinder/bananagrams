# Generated by Django 3.1.2 on 2020-10-03 06:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0017_auto_20201003_0441'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='event_type',
            field=models.CharField(choices=[('CREATE', 'CREATE'), ('START', 'START'), ('JOIN', 'JOIN'), ('PEEL', 'PEEL'), ('DUMP', 'DUMP'), ('BANANAS', 'BANANAS'), ('WIN', 'WIN'), ('ROTTEN', 'ROTTEN'), ('FULL', 'FULL')], default='CREATE', max_length=10),
        ),
        migrations.AlterField(
            model_name='game',
            name='remaining_tiles',
            field=models.CharField(default='QNSNHMGDNYFAXIOEEEEIUEHMLRMZBSAWIEONSTIIATPEDAIAQORIXTJEOUDYWORGELRINRAFNTEATTCSPGWDUIEGNKLLOBRKVTIOETRESRLAOYDSOJEEAUEVVTNRCAHEAPOCZOEDBAFAIUIU', max_length=144),
        ),
        migrations.AlterField(
            model_name='game',
            name='url_key',
            field=models.CharField(default='smO07nFRbL2h2RSJy526', max_length=100),
        ),
    ]
