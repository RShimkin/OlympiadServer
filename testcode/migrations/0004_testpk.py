# Generated by Django 4.0.1 on 2022-03-06 06:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('testcode', '0003_profile_region'),
    ]

    operations = [
        migrations.CreateModel(
            name='TestPk',
            fields=[
                ('num', models.IntegerField(default=1, primary_key=True, serialize=False)),
                ('content', models.CharField(max_length=200, verbose_name='Тестовый ввод')),
            ],
            options={
                'managed': True,
            },
        ),
    ]