# Generated by Django 5.0.7 on 2024-07-16 13:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_alter_user_apellidos_alter_user_nombres'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='user',
            options={},
        ),
        migrations.AlterField(
            model_name='user',
            name='apellidos',
            field=models.CharField(blank=True, max_length=30),
        ),
        migrations.AlterField(
            model_name='user',
            name='nombres',
            field=models.CharField(blank=True, max_length=30),
        ),
        migrations.AlterField(
            model_name='user',
            name='username',
            field=models.CharField(max_length=10, unique=True),
        ),
    ]
