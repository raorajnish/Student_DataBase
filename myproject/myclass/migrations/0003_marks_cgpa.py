# Generated by Django 5.1 on 2024-08-31 04:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myclass', '0002_alter_student_slug2'),
    ]

    operations = [
        migrations.AddField(
            model_name='marks',
            name='cgpa',
            field=models.FloatField(blank=True, default=0, null=True),
        ),
    ]
