# Generated by Django 3.2.8 on 2022-06-17 20:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('manager', '0011_auto_20220617_1549'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='venda',
            name='produtos_comprados',
        ),
        migrations.RemoveField(
            model_name='venda',
            name='qtds_compradas',
        ),
    ]
