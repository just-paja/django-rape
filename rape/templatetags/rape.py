from django.core.urlresolvers import reverse
from django import template
from .. import helpers, settings

register = template.Library()


def rape_url(url):
	return helpers.rape_static_url(url)


def raped_script(name):
	return reverse('raped_script', args=[settings.RAPE_SERIAL, name])


def raped_style(name):
	return reverse('raped_style', args=[settings.RAPE_SERIAL, name])


def tag_script(name):
	return '<script type="text/javascript" src="%s"></script>' % (raped_script(name))


def tag_style(name):
	return '<link rel="stylesheet" type="text/css" href="%s">' % (raped_style(name))


def rape_static_url(url, request=None):
	return helpers.rape_static_url(url, request)


register.simple_tag(rape_url)
register.simple_tag(rape_static_url)
register.simple_tag(raped_script)
register.simple_tag(raped_style)
register.simple_tag(tag_script)
register.simple_tag(tag_style)
