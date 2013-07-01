from datetime import timedelta
import os, time, settings, helpers, re


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
	return '%s/%s/%s.%s' % (settings.RAPE_PATH, res_type, res_name, get_postfix(res_type, True))


def get_output_name(res_type, name):
	arg = 'plain'
	if settings.RAPE_PACK: arg = 'packed'
	return 'rape/%s/%s.%s.%s.%s' % (res_type, name, arg, settings.RAPE_SERIAL, get_postfix(res_type))


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
	return rape_resource_url(matchobj.group(1))


def replace_resource_urls(string):
	return re.sub(r'\{\%\sraped_url\s[\'\"]?([\/a-z0-9\.\-\_]+)[\'\"]?\s\%\}', get_resource_url_from_match ,string, flags=re.IGNORECASE)


def rape_resource_url(url)
	return '%s?serial=%d' % (url, settings.RAPE_SERIAL)
