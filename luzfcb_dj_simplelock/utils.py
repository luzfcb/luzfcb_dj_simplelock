# -*- coding: utf-8 -*-
from __future__ import unicode_literals


def get_label(model_instance):
    """
    :param model_instance:
    :return:
    """
    app_name = model_instance._meta.app_label  # NOQA
    model_name = str(model_instance.__class__.__name__).lower()
    return '{app_name}.{model_name}'.format(app_name=app_name, model_name=model_name)
