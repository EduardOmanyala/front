# Generated by Django 4.2.6 on 2024-02-11 22:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('frontmain', '0004_alter_order_subject'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='time_paid',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='order',
            name='pages',
            field=models.IntegerField(default=1),
        ),
    ]
