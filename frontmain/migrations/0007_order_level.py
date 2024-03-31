# Generated by Django 4.2.6 on 2024-02-26 13:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('frontmain', '0006_order_deadline'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='level',
            field=models.CharField(blank=True, choices=[('High School', 'High School'), ('College', 'College'), ('Masters', 'Masters'), ('PhD', 'PhD')], default='College', max_length=500, null=True),
        ),
    ]