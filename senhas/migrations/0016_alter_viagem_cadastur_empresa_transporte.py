# Generated by Django 3.2.10 on 2022-03-18 19:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('senhas', '0015_auto_20220318_1428'),
    ]

    operations = [
        migrations.AlterField(
            model_name='viagem',
            name='cadastur_empresa_transporte',
            field=models.CharField(max_length=18),
        ),
    ]