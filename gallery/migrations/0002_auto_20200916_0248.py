# Generated by Django 3.0.5 on 2020-09-16 05:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gallery', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gallery',
            name='url_clean',
            field=models.SlugField(max_length=255, unique_for_date='publish', verbose_name='Url_Clean'),
        ),
    ]