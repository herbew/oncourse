# Generated by Django 3.2.16 on 2022-12-08 07:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('masters', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='answer',
            name='option',
            field=models.CharField(blank=True, choices=[('', 'Multiple-choice'), ('A', 'A'), ('B', 'B'), ('C', 'C'), ('D', 'D'), ('E', 'E')], db_index=True, max_length=1, null=True, verbose_name='Option'),
        ),
    ]
