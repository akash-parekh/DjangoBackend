# Generated by Django 4.2.4 on 2023-08-28 14:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboardApi', '0002_document_total_time_alter_document_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='document',
            name='time_to_process',
            field=models.CharField(blank=True, editable=False, max_length=10),
        ),
        migrations.AddField(
            model_name='document',
            name='time_to_review',
            field=models.CharField(blank=True, editable=False, max_length=10),
        ),
    ]
