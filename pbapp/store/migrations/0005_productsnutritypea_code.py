# Generated by Django 2.2.2 on 2019-06-20 20:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0004_remove_productsnutritypea_code'),
    ]

    operations = [
        migrations.AddField(
            model_name='productsnutritypea',
            name='code',
            field=models.CharField(default='00', max_length=500),
        ),
    ]
