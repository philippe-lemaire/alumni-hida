# Generated by Django 4.2.4 on 2023-09-25 09:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trombinoscope', '0006_alter_customuser_photo'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customuser',
            name='enseignant_hida',
        ),
        migrations.RemoveField(
            model_name='customuser',
            name='looking_for_internship',
        ),
        migrations.AddField(
            model_name='customuser',
            name='bio',
            field=models.TextField(blank=True, max_length=1000, verbose_name='Biographie'),
        ),
    ]
