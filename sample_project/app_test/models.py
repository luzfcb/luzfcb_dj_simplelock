from django.db import models


class Person(models.Model):
    nome = models.CharField(max_length=255, blank=True, null=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    class Meta:
        app_label = 'app_test'
