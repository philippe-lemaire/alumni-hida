# Generated by Django 4.2.4 on 2023-09-27 09:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trombinoscope', '0009_rename_bio_customuser_occupation_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='photo',
            field=models.ImageField(blank=True, default='photos/default.webp', upload_to='photos/'),
        ),
    ]
