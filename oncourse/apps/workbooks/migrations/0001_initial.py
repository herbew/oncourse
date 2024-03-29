# Generated by Django 3.2.16 on 2022-12-08 05:34

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django_extensions.db.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='UserTraceability',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
                ('typed', models.CharField(blank=True, choices=[('001', 'Admin'), ('002', 'Mentor'), ('003', 'Student')], max_length=3, null=True, verbose_name='Type')),
                ('user_update', models.CharField(blank=True, db_index=True, max_length=30, null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='User')),
            ],
            options={
                'verbose_name': 'UserTraceability',
                'verbose_name_plural': '001 Workbooks User Traceability',
                'unique_together': {('user', 'typed')},
            },
        ),
    ]
