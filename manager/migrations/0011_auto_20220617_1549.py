# Generated by Django 3.2.8 on 2022-06-17 18:49

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('manager', '0010_venda_valor_total'),
    ]

    operations = [
        migrations.AddField(
            model_name='venda',
            name='produtos_comprados',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.IntegerField(null=True), null=True, size=20),
        ),
        migrations.AddField(
            model_name='venda',
            name='qtds_compradas',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.IntegerField(null=True), null=True, size=20),
        ),
        migrations.AlterField(
            model_name='venda',
            name='valor_total',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=8, verbose_name='Valor total'),
        ),
    ]