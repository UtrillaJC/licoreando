# Generated by Django 2.0.8 on 2019-01-18 12:04

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Categoria',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.TextField(unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Licor',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('codigoReferencia', models.TextField(blank=True, null=True)),
                ('titulo', models.TextField(blank=True, null=True)),
                ('descripcion', models.TextField(blank=True, null=True)),
                ('precio', models.FloatField(blank=True, null=True)),
                ('origen', models.TextField(blank=True, null=True)),
                ('cantidad', models.TextField(blank=True, null=True)),
                ('graduacion', models.FloatField(blank=True, null=True)),
                ('urlProducto', models.URLField(unique=True)),
                ('urlImagen', models.URLField(blank=True, null=True)),
                ('enStock', models.BooleanField()),
            ],
        ),
        migrations.AddField(
            model_name='categoria',
            name='licor',
            field=models.ManyToManyField(blank=True, to='licor.Licor'),
        ),
    ]
