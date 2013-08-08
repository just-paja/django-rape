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


def rape_static_url(url, request=None):
	return helpers.rape_static_url(url, request)


register.simple_tag(rape_url)
register.simple_tag(rape_static_url)
register.simple_tag(raped_script)
register.simple_tag(raped_style)
