# Generated by Django 3.1.7 on 2021-03-21 20:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('equipamentos', '0002_auto_20210321_1741'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='tipo_equipamento',
            options={'ordering': ['descricao'], 'verbose_name': 'Tipo de Equipamento', 'verbose_name_plural': 'Tipos de Equipamentos'},
        ),
    ]