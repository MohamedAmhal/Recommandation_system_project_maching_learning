# Generated by Django 5.0.4 on 2024-05-03 11:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('application', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productreview',
            name='product',
            field=models.TextField(default=True),
        ),
    ]
