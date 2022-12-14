from django import template

register = template.Library()


@register.filter('in_group')
def in_group(user, group_name):
    if user and user.is_authenticated:
        if group_name:
            return user.groups.filter(name=group_name).exists()

    return False
