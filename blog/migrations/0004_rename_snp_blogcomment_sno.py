# Generated by Django 3.2.7 on 2021-09-28 16:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_blogcomment'),
    ]

    operations = [
        migrations.RenameField(
            model_name='blogcomment',
            old_name='snp',
            new_name='sno',
        ),
    ]
