# Generated by Django 2.2 on 2020-03-14 18:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('grade', '0003_auto_20200314_0941'),
    ]

    operations = [
        migrations.RenameField(
            model_name='assignment',
            old_name='uploder',
            new_name='uploader',
        ),
    ]