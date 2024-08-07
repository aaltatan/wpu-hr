from django import template
register = template.Library()

@register.simple_tag
def get_verbose_field_name(instance, field_name):
    """
    Returns verbose_name for a field.
    """
    if instance:
        return instance._meta.get_field(field_name).verbose_name.title()
    else:
        return ''