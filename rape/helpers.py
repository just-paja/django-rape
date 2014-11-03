from datetime import timedelta
from django.core.urlresolvers import reverse
from functools import partial
import os, time, settings, helpers, re, json, glob


TAG_MATCH_DEFAULT = '[\'\"]?([\/a-zA-Z0-9\.\-\_\?\#]+)[\'\"]?'


"""
Get file list for predefined resource.

* res_type string Resource type ('style', 'script')
* name     string Name of the resource defined in settings.RAPED_(STYLES|SCRIPTS)

Returns list of paths
"""
def get_file_list(res_type, name, medium = None):
	if not medium:
		medium = settings.RAPED_SCRIPTS
		if res_type == 'style': medium = settings.RAPED_STYLES

	files = medium[name]
	file_list = []

	for fp in files:
		file_list += checkout_file(res_type, '%s/%s' % (settings.RAPE_PATH, fp))

	return file_list


"""
Check resource path and try to include all resources if directory. When passed
path to directory with package.json or bower.json, it reads metadata and
includes correct file paths

* res_type Is string defining resource type ('style', 'script')
* fp_in    Is path. Could be absolute from fs root or relative.

Returns list of paths
"""
def checkout_file(res_type, fp_in):
	post  = get_postfix(res_type, True)
	files = []
	fp    = fp_in
	fp_p  = '%s.%s' % (fp, post)
	dirs  = False

	if re.search('\/$', fp):
		dirs = True


	# Prefer files with postfix over other
	if dirs:
		if not os.path.exists(fp):
			fp = fp_p
	else:
		if os.path.exists(fp_p) and os.path.isfile(fp_p):
			fp = fp_p


	# User passed path that exists
	if os.path.exists(fp):
		fp_path = fp


		# It is a symlink, lookup its' real path
		if os.path.islink(fp_path):
			fp_path = os.path.realpath(fp_path)


		# User passed direct path to a file
		if os.path.isfile(fp_path):
			files.append(fp_path)


		# It is a directory
		elif os.path.isdir(fp_path):
			path_bow = '%s/bower.json' % fp_path
			path_pkg = '%s/package.json' % fp_path
			path_cmp = '%s/component.json' % fp_path

			has_bow = os.path.exists(path_bow)
			has_pkg = os.path.exists(path_pkg)
			has_cmp = os.path.exists(path_cmp)

			if not has_bow:
				path_bow = '%s/.bower.json' % fp_path
				has_bow = os.path.exists(path_bow)


			# Look for bower.json and include file defined as key 'main'
			if has_bow:
				point = open(path_bow)
				meta  = json.loads(point.read())
				point.close()

				if 'main' in meta:
					main = meta['main']

					if not type(main) is list:
						main = [main]

					for main_fp in main:
						files += checkout_file(res_type, '%s/%s' % (fp, main_fp))

				elif 'include' in meta:
					for fp_pkg in meta['include']:
						files += checkout_file(res_type, '%s/%s' % (fp, fp_pkg))

				# We have walked trough bower.json but found nothing useful
				else:
					has_bow = False


			# Look for component.json and include files defined as key 'scripts'
			if has_cmp and not has_bow:
				point = open(path_cmp)
				meta  = json.loads(point.read())
				point.close()

				# Key scripts should be list
				if 'scripts' in meta:
					for fp_pkg in meta['scripts']:
						files += checkout_file(res_type, '%s/%s' % (fp, fp_pkg))

				# We have walked trough component.json but found nothing useful
				else:
					has_cmp = False


			# Look for package.json and include all files defined as key 'include'
			if has_pkg and not (has_bow or has_cmp):
				point = open(path_pkg)
				meta  = json.loads(point.read())
				point.close()

				# Ignore key 'main', we can't do requires
				if 'include' in meta:
					for fp_pkg in meta['include']:
						files += checkout_file(res_type, '%s/%s' % (fp, fp_pkg))

				# We have walked trough package.json but found nothing useful
				else:
					raise Exception('Found "package.json" but "include" is not defined in %s.' % path_pkg)


			# No bower.json or package.json was found. Include whole directory
			if not (has_bow or has_pkg):
				found  = glob.glob('%s/**' % (fp_path))
				append = []

				for key,fp_child in enumerate(found):
					if os.path.isdir(fp_child):

						# Append trailing "/" to the end of path to this method knows we
						# prefer checking out whole directory over files with identical name
						append += checkout_file(res_type, "%s/" % fp_child)

					elif os.path.islink(fp_child):
						found.pop(key)
					else:
						append += [fp_child]

				files += append

	# Nope, this file really can't be included
	else:
		raise Exception('Couldn\'t find %s resource named "%s"' % (res_type, fp_in))

	return files



"""
Has this predefined resource changed since its' last compilation?

* request  request
* res_type string  Resource type ('script', 'style')
* name     string Name of the resource defined in settings.RAPED_(STYLES|SCRIPTS)

Returns bool
"""
def changed(request, res_type, name, medium = None):
	file_name = get_output_path(request, res_type, name)
	changed = False

	# Check if the resource is compiled
	if os.path.isfile(file_name):
		last_change = os.path.getmtime(file_name)
		file_list = get_file_list(res_type, name, medium)

		# Walk trough all files from this resource
		for res_name in file_list:
			res_path = res_name
			res_last_change = os.path.getmtime(res_path)

			if res_last_change > last_change:
				changed = True
				break

	# It is not compiled, so we can act as it has changed
	else:
		changed = True

	return changed


"""
Get name of raped resource - output file

* request  request
* res_type string  Resource type ('script', 'style')
* name     string Name of the resource defined in settings.RAPED_(STYLES|SCRIPTS)

Returns string, a relative path from static directory
"""
def get_output_name(request, res_type, name):
	protocol = 'http'
	arg = 'plain'

	if request.is_secure(): protocol = 'https'
	if settings.RAPE_PACK: arg = 'packed'

	return 'rape/%s/%s/%s-%s-%s.%s.%s' % (res_type, name, protocol, request.META['HTTP_HOST'], arg, settings.RAPE_SERIAL, get_postfix(res_type))


"""
Get path for raped resource

* request  request
* res_type string  Resource type ('script', 'style')
* name     string Name of the resource defined in settings.RAPED_(STYLES|SCRIPTS)

Returns string, an absolute path to static directory
"""
def get_output_path(request, res_type, name):
	return '%s/%s' % (settings.STATIC_ROOT, get_output_name(request, res_type, name))


"""
Get absolute URL for raped resource

* res_type string  Resource type ('script', 'style')
* name     string Name of the resource defined in settings.RAPED_(STYLES|SCRIPTS)

Returns string, an absolute path from domain root excluding host
"""
def get_output_url(res_type, name):
	return '%s%s' % (settings.STATIC_URL, get_output_name(res_type, name))


"""
Get postfix for resource type

* res_type string  Resource type ('script', 'style')
* home     bool    Should it be postfix that it's compiled from?

Returns string, an absolute path to static directory
"""
def get_postfix(res_type, home=False):
	postfix = 'js'
	if res_type == 'style':
		if home: postfix = 'scss'
		else: postfix = 'css'

	return postfix


def exists(res_type, name, medium=None):
	if not medium:
		medium = settings.RAPED_SCRIPTS
		if res_type == 'style': medium = settings.RAPED_STYLES

	return name in medium


def get_content_type(res_type):
	header = 'text/javascript; charset=utf-8'
	if res_type == 'style': header = 'text/css'
	return header


def add_host(url, request):
	if request:
		protocol = 'http'
		if request.is_secure(): protocol = 'https'

		url = '%s://%s%s' % (protocol, request.META['HTTP_HOST'], url)

	return url


"""
Replaces resource {% %} tag values inside the requested resource content

* rq     request Resource request
* string string  Resource content
* returns string Content with replaced values

"""
def replace_resource_urls(rq, string):
	tags = settings.RAPE_TAGS

	for tag in tags:
		tag_match = TAG_MATCH_DEFAULT

		if 'match' in tag:
			tag_match = tag['match']

		# Set up regex rule to match "{% tag_name predefined_match %}"
		rule = '\{\%%\s?%s\s%s\s?\%%\}' % (tag['tag'], tag_match)

		# Module path for replace function
		path = tag['replace'].split('.')

		# Replace function name
		name = path.pop()

		# Import replace function module and function
		mod  = __import__('.'.join(path), fromlist=[''])
		fn   = getattr(mod, name)

		string = re.sub(rule, partial(fn, rq=rq), string)

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
