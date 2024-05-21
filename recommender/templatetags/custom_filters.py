from django import template

register = template.Library()

@register.filter
def truncate_chars(value, max_length):
	if len(value) > max_length:
		return value[:max_length - 3] + '...'
	return value

@register.filter(name='replace')
def replace(value, args):
    old, new = args.split(',')
    return value.replace(old, new)