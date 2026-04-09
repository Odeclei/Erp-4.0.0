from django import template

register = template.Library()


@register.filter
def mul(value, arg):
    """Multiplica value por arg"""
    try:
        return float(value) * float(arg)
    except (ValueError, TypeError):
        return None


@register.filter
def div(value, arg):
    """Divide value por arg"""
    try:
        if float(arg) == 0:
            return None
        return float(value) / float(arg)
    except (ValueError, TypeError):
        return None
