# Generated by Django 5.0.1 on 2024-01-28 23:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('frontmain', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='subject',
            field=models.CharField(max_length=500),
        ),
    ]
