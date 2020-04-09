def get_class_upper_variables(cls_object):
    return [value for name, value in vars(cls_object).items() if name.isupper()]
