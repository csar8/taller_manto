# Generated by Django 5.0.3 on 2024-05-23 10:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('utaller', '0019_rename_clave_registro_factura_clave_de_registro_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='factura',
            name='concepto',
            field=models.CharField(max_length=100),
        ),
    ]
