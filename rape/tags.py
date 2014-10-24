from django.core.urlresolvers import reverse
from helpers import add_host, rape_static_url
import settings


def raped_url(matchobj, rq=None):
	return rape_static_url(matchobj.group(1), rq)


def raped_script(matchobj, rq=None):
	return add_host(reverse('raped_script', args=[settings.RAPE_SERIAL, matchobj.group(1)]), rq)


def raped_style(matchobj, rq=None):
	return add_host(reverse('raped_style', args=[settings.RAPE_SERIAL, matchobj.group(1)]), rq)
