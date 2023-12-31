# Generated by Django 4.2.4 on 2023-10-27 09:44

from django.db import migrations, models
import file_validator.models


class Migration(migrations.Migration):

    dependencies = [
        ('trombinoscope', '0012_alter_customuser_photo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='photo',
            field=models.ImageField(blank=True, upload_to='photos/', validators=[file_validator.models.DjangoFileValidator(acceptable_mimes=['image/png', 'image/jpeg', 'image/jpg', 'image/webp'], acceptable_types=['image'], libraries=['python_magic', 'filetype'], max_upload_file_size=5242880)]),
        ),
    ]
