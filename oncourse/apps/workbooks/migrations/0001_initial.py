# Generated by Django 3.2.16 on 2022-12-07 13:52

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django_extensions.db.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='StudentEventTask',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
                ('no', models.IntegerField(verbose_name='No')),
                ('no_en_us', models.IntegerField(null=True, verbose_name='No')),
                ('no_ja', models.IntegerField(null=True, verbose_name='No')),
                ('no_ar', models.IntegerField(null=True, verbose_name='No')),
                ('no_ko', models.IntegerField(null=True, verbose_name='No')),
                ('no_hi', models.IntegerField(null=True, verbose_name='No')),
                ('no_es', models.IntegerField(null=True, verbose_name='No')),
                ('score', models.IntegerField(default='0')),
                ('user_update', models.CharField(blank=True, db_index=True, max_length=30, null=True)),
                ('student_event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='academics.studentevent', verbose_name='Student Event')),
                ('task', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='masters.task', verbose_name='Task')),
            ],
            options={
                'verbose_name': 'StudentEventTask',
                'verbose_name_plural': '003 Workbooks Student Event Task',
                'unique_together': {('student_event', 'task')},
            },
        ),
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
        migrations.CreateModel(
            name='StudentEventTaskAnswer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
                ('user_update', models.CharField(blank=True, db_index=True, max_length=30, null=True)),
                ('answer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='masters.answer', verbose_name='Answer')),
                ('student_event_task', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='workbooks.studenteventtask', verbose_name='Student Event Task')),
            ],
            options={
                'verbose_name': 'StudentEventTaskAnswer',
                'verbose_name_plural': '004 Workbooks Student Event Task Answer',
                'unique_together': {('student_event_task', 'answer')},
            },
        ),
    ]
