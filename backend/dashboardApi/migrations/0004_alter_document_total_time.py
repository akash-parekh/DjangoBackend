# Generated by Django 4.2.4 on 2023-08-28 14:41

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('dashboardApi', '0003_document_time_to_process_document_time_to_review'),
    ]

    operations = [
        migrations.AlterField(
            model_name='document',
            name='total_time',
            field=models.CharField(blank=True, default=django.utils.timezone.now, editable=False, max_length=10),
            preserve_default=False,
        ),
    ]