def get_label(model_instance):
    """
    :param model_instance:
    :return:
    """
    return '{app_name}.{model_name}'.format(app_name=model_instance._meta.app_label,
                                            model_name=str(model_instance.__class__.__name__).lower())
