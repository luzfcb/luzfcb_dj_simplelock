from django.db import models


class Person(models.Model):
    nome = models.CharField(max_length=255, blank=True, null=True)
