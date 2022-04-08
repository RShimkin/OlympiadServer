from django.db import models

class Person(models.Model):
    name = models.CharField(max_length=255, verbose_name="ИмяЫ")
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="URL")
