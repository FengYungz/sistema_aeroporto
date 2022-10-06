# Generated by Django 4.1.2 on 2022-10-06 20:00

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Funcionario',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('nome', models.CharField(max_length=200)),
                ('cpf', models.CharField(max_length=11)),
                ('cargo', models.CharField(max_length=200)),
            ],
            options={
                'db_table': 'Funcionarios',
            },
        ),
        migrations.CreateModel(
            name='Voo',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('codigo', models.CharField(max_length=12, unique=True)),
                ('companhia', models.CharField(max_length=150)),
                ('previsao_chegada', models.DateTimeField()),
                ('previsao_partida', models.DateTimeField()),
                ('data_chegada', models.DateTimeField(null=True)),
                ('data_saida', models.DateTimeField(null=True)),
                ('status', models.CharField(max_length=20)),
                ('rota', models.CharField(max_length=200)),
            ],
            options={
                'db_table': 'Voos',
            },
        ),
    ]
