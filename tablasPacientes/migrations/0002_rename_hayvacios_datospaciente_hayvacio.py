# Generated by Django 3.2.9 on 2022-02-04 20:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tablasPacientes', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='datospaciente',
            old_name='hayVacios',
            new_name='hayVacio',
        ),
    ]
