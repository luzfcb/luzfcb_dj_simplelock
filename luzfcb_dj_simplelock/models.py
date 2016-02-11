# -*- coding: utf-8 -*-
from django.conf import settings
from django.db import models

from django.utils import timezone

USER_MODEL = getattr(settings, 'AUTH_USER_MODEL', 'auth.User')


class ObjectLock(models.Model):
    bloqueado_em = models.DateTimeField(default=timezone.now, blank=True, editable=False)
    bloqueado_por = models.ForeignKey(to=USER_MODEL,
                                      related_name="%(app_label)s_%(class)s_bloqueado_por", null=True,
                                      blank=True, on_delete=models.SET_NULL, editable=False)
    bloqueado_por_user_name = models.CharField(blank=True, max_length=500, editable=False)
    bloqueado_por_full_name = models.CharField(blank=True, max_length=500, editable=False)
    #    session_key = models.CharField('session key', max_length=40, null=True,
    #                                   blank=True, editable=False)

    expire_date = models.DateTimeField('expire date')

    app_and_model = models.CharField(max_length=350, editable=False, blank=True)
    model_pk = models.IntegerField(null=True,
                                   blank=True, editable=False, db_index=True)
