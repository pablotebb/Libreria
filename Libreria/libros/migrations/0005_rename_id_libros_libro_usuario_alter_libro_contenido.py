# Generated by Django 5.2.1 on 2025-05-18 16:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('libros', '0004_alter_libro_contenido'),
    ]

    operations = [
        migrations.RenameField(
            model_name='libro',
            old_name='id_libros',
            new_name='usuario',
        ),
        migrations.AlterField(
            model_name='libro',
            name='contenido',
            field=models.TextField(),
        ),
    ]
