# Generated by Django 5.1.3 on 2024-11-15 10:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('file_api', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='entry',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]
