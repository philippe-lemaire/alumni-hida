# Generated by Django 4.2.4 on 2023-09-24 07:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trombinoscope', '0005_alter_customuser_photo_alter_customuser_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='photo',
            field=models.ImageField(blank=True, upload_to='photos/'),
        ),
    ]
