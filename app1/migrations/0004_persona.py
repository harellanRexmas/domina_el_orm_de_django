# Generated by Django 4.0.3 on 2022-03-13 21:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0003_categoria_estado'),
    ]

    operations = [
        migrations.CreateModel(
            name='Persona',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('estado', models.CharField(choices=[('Activo', 'activo'), ('Inactivo', 'Inactivo')], default='Activo', max_length=8)),
                ('fecha_creacion', models.DateTimeField(auto_now_add=True)),
                ('fecha_modificacion', models.DateTimeField(auto_now=True)),
                ('activo', models.BooleanField(default=True)),
                ('nombre', models.CharField(max_length=50)),
                ('apellido', models.CharField(max_length=50)),
                ('fecha_nacimiento', models.DateField()),
            ],
            options={
                'verbose_name_plural': 'Personas',
            },
        ),
    ]
