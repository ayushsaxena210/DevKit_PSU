# Generated by Django 4.0.4 on 2022-05-24 19:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('TemplateTool', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project_record',
            name='yaml_file',
            field=models.CharField(blank=True, max_length=40, null=True),
        ),
    ]