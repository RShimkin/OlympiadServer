# Generated by Django 4.0.1 on 2022-03-08 07:16

from django.db import migrations, models
import djongo.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('testcode', '0005_testdata'),
    ]

    operations = [
        migrations.CreateModel(
            name='TestJson',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', djongo.models.fields.JSONField()),
            ],
        ),
    ]
