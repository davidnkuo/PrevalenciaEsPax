# Generated by Django 3.2.9 on 2022-02-04 21:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tablasPacientes', '0012_auto_20220204_1828'),
    ]

    operations = [
        migrations.AlterField(
            model_name='datosespax',
            name='tipo',
            field=models.CharField(blank=True, choices=[(1, 'No radiográfica'), (2, 'Radiográfica')], default='', max_length=10),
        ),
    ]