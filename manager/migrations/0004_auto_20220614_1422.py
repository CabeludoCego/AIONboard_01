# Generated by Django 3.2.8 on 2022-06-14 17:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('manager', '0003_auto_20220613_2147'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='produto',
            name='data',
        ),
        migrations.AddField(
            model_name='produto',
            name='imagem',
            field=models.ImageField(blank=True, height_field=400, null=True, upload_to='BASE_DIR/media/imgs', width_field=400),
        ),
    ]
