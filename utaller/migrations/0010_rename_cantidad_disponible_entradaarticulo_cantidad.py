# Generated by Django 5.0.3 on 2024-05-16 06:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('utaller', '0009_rename_cantidad_entradaarticulo_cantidad_disponible_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='entradaarticulo',
            old_name='cantidad_disponible',
            new_name='cantidad',
        ),
    ]
