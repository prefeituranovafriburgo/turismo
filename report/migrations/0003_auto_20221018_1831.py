# Generated by Django 3.1.4 on 2022-10-18 21:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('report', '0002_alter_problemasrelatados_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='problemasrelatados',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]