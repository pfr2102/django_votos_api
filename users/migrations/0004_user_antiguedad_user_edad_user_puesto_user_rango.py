# Generated by Django 4.2.9 on 2024-02-20 06:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_alter_user_email'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='antiguedad',
            field=models.CharField(blank=True, max_length=3, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='edad',
            field=models.CharField(blank=True, max_length=3, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='puesto',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='rango',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
