# Generated by Django 3.2.16 on 2023-04-02 17:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('school', '0002_remove_schoolfee_term'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='active',
            field=models.BooleanField(default=True, help_text='Is the student active?', verbose_name='Active'),
        ),
    ]
