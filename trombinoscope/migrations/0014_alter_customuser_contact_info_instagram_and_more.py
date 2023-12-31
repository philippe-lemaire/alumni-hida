# Generated by Django 4.2.4 on 2023-10-28 14:19

from django.db import migrations, models
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    dependencies = [
        ('trombinoscope', '0013_alter_customuser_photo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='contact_info_instagram',
            field=models.URLField(blank=True, verbose_name='Adresse compte instagram'),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='contact_info_tel',
            field=phonenumber_field.modelfields.PhoneNumberField(blank=True, max_length=128, region='FR', verbose_name='Numéro de téléphone'),
        ),
    ]
