# Generated by Django 4.2.9 on 2024-02-20 21:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('etapa', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='etapa',
            old_name='nombre_estapa',
            new_name='nombre_etapa',
        ),
    ]