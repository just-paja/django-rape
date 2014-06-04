from django.core.urlresolvers import reverse
from django import template
from .. import helpers, settings

register = template.Library()


def rape_url(url, request=None):
	return helpers.rape_static_url(url, request)


def raped_script(name, request=None):
	return helpers.add_host(reverse('raped_script', args=[settings.RAPE_SERIAL, name]), request)


def raped_style(name, request=None):
	return helpers.add_host(reverse('raped_style', args=[settings.RAPE_SERIAL, name]), request)


def tag_script(name, request=None):
	return '<script type="text/javascript" src="%s"></script>' % (raped_script(name, request))


def tag_style(name, request=None):
	return '<link rel="stylesheet" type="text/css" href="%s">' % (raped_style(name, request))


def rape_static_url(url, request=None):
	return helpers.rape_static_url(url, request)


register.simple_tag(rape_url)
register.simple_tag(rape_static_url)
register.simple_tag(raped_script)
register.simple_tag(raped_style)
register.simple_tag(tag_script)
register.simple_tag(tag_style)
