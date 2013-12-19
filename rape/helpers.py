from datetime import timedelta
import os, time, settings, helpers, re
from django.core.urlresolvers import reverse


def get_file_list(res_type, name):
	medium = settings.RAPED_SCRIPTS

	if res_type == 'style': medium = settings.RAPED_STYLES

	return medium[name]


def changed(res_type, name):
	file_name = get_output_path(res_type, name)
	changed = False

	if os.path.isfile(file_name):
		last_change = os.path.getmtime(file_name)
		file_list = get_file_list(res_type, name)

		for res_name in file_list:
			res_path = get_res_name(res_type, res_name)
			res_last_change = os.path.getmtime(res_path)

			if res_last_change > last_change:
				changed = True
				break

	else:
		changed = True

	return changed


def get_res_name(res_type, res_name):
	return '%s/%s.%s' % (settings.RAPE_PATH, res_name, get_postfix(res_type, True))


def get_output_name(res_type, name):
	arg = 'plain'
	if settings.RAPE_PACK: arg = 'packed'
	return 'rape/%s/%s/%s.%s.%s' % (res_type, name, arg, settings.RAPE_SERIAL, get_postfix(res_type))


def get_output_path(res_type, name):
	return '%s/%s' % (settings.STATIC_ROOT, get_output_name(res_type, name))


def get_output_url(res_type, name):
	return '%s%s' % (settings.STATIC_URL, get_output_name(res_type, name))


def get_postfix(res_type, home=False):
	postfix = 'js'
	if res_type == 'style':
		if home: postfix = 'scss'
		else: postfix = 'css'

	return postfix


def exists(res_type, name):
	medium = settings.RAPED_SCRIPTS
	if res_type == 'style': medium = settings.RAPED_STYLES

	return name in medium


def get_content_type(res_type):
	header = 'text/javascript; charset=utf-8'
	if res_type == 'style': header = 'text/css'
	return header


def get_resource_url_from_match(matchobj):
	return rape_static_url(matchobj.group(1))


def get_raped_script_url_from_match(matchobj):
	return reverse('raped_script', args=[settings.RAPE_SERIAL, matchobj.group(1)])


def get_raped_style_url_from_match(matchobj):
	return reverse('raped_style', args=[settings.RAPE_SERIAL, matchobj.group(1)])


def replace_resource_urls(string):
	string = re.sub(r'\{\%\sraped_url\s[\'\"]?([\/a-zA-Z0-9\.\-\_\?\#]+)[\'\"]?\s\%\}', get_resource_url_from_match, string)
	string = re.sub(r'\{\%\sraped_script\s[\'\"]?([\/a-zA-Z0-9\.\-\_\?\#]+)[\'\"]?\s\%\}', get_raped_script_url_from_match, string)
	string = re.sub(r'\{\%\sraped_style\s[\'\"]?([\/a-zA-Z0-9\.\-\_\?\#]+)[\'\"]?\s\%\}', get_raped_style_url_from_match, string)
	return string


def rape_static_url(url, request=None):
	if request:
		if request.is_secure(): protocol = 'https'
		else: protocol = 'http'

		return "%s://%s%s%s/%s?serial=%s" % (
			protocol,
			request.META['HTTP_HOST'],
			settings.STATIC_URL,
			settings.RAPE_PROJECT_NAME,
			url,
			settings.RAPE_SERIAL
		)
	else:
		return "%s%s/%s?serial=%s" % (settings.STATIC_URL, settings.RAPE_PROJECT_NAME, url, settings.RAPE_SERIAL)


def check_dirs(res_type):
	check_dir("%s" % settings.STATIC_ROOT)
	check_dir("%s/rape" % settings.STATIC_ROOT)
	check_dir("%s/rape/%s" % (settings.STATIC_ROOT, res_type))


def check_dir(path):
	if not os.path.exists(path):
		try:
			os.makedirs(path)
		except OSError as exception:
			if exception.errno != errno.EEXIST:
				raise
