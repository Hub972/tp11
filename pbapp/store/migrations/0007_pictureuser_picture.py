# Generated by Django 2.2.2 on 2019-10-20 10:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0006_pictureuser'),
    ]

    operations = [
        migrations.AddField(
            model_name='pictureuser',
            name='picture',
            field=models.ImageField(null=True, upload_to='pic/'),
        ),
    ]