import os
from django.conf import settings

ROOT = getattr(settings, 'ROOT', os.path.abspath(os.path.dirname(__file__)))

RAPED_SCRIPTS = getattr(settings, 'RAPED_SCRIPTS', {})

RAPED_STYLES = getattr(settings, 'RAPED_STYLES', {})

RAPE_PACK = getattr(settings, 'RAPE_PACK', False)

RAPE_SERIAL = getattr(settings, 'RAPE_SERIAL', 1)

RAPE_PATH = getattr(settings, 'RAPE_PATH', '%s/rape' % settings.ROOT)

RAPE_PROJECT_NAME = getattr(settings, 'PROJECT_NAME')

STATIC_ROOT = getattr(settings, 'STATIC_ROOT')

STATIC_URL = getattr(settings, 'STATIC_URL')

RAPE_CORS_ORIGIN  = getattr(settings, 'RAPE_CORS_ORIGIN', None)

RAPE_CORS_METHODS = getattr(settings, 'RAPE_CORS_METHODS', None)

RAPE_CORS_HEADERS = getattr(settings, 'RAPE_CORS_METHODS', None)

"""
Define what tags should be replaced inside resources.

{
	# This is the part behind {%. "{% tag_name ... %}"
	'tag':'name_of_tag_that_will_be_replaced',

	# Method will receive matchobj and rq as parameters
	'replace':'absolute.path.for.replacement.method',

	# This string will be used for regex matching arguments of the tag
	'match':'regex+(like)+string'
}

"""
RAPE_TAGS = getattr(settings, 'RAPE_TAGS', [
	{
		'tag':'raped_url',
		'replace':'rape.tags.raped_url'
	},

	{
		'tag':'raped_script',
		'replace':'rape.tags.raped_script'
	},

	{
		'tag':'raped_style',
		'replace':'rape.tags.raped_style'
	}
])
