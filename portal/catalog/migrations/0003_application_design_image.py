# Generated by Django 5.1.3 on 2024-11-09 04:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0002_alter_application_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='application',
            name='design_image',
            field=models.ImageField(blank=True, null=True, upload_to='admin', verbose_name='Изображение дизайна'),
        ),
    ]
