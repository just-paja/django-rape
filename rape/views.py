from django.http import HttpResponse, HttpResponseRedirect, Http404, HttpResponseForbidden
from django.core.urlresolvers import reverse
from packers import script, style
import re, os, time, settings, helpers


def resource(request, serial, name, res_type):
	if int(serial) == settings.RAPE_SERIAL:
		if helpers.exists(res_type, name):
			if helpers.changed(request, res_type, name):
				helpers.check_dirs(res_type)
				generate_resource(request, res_type, name)

			fp = open(helpers.get_output_path(request, res_type, name))
			response = HttpResponse(re.sub(r'{{HOST}}', request.META['HTTP_HOST'], fp.read()))
			fp.close()

			if settings.RAPE_CORS_ORIGIN:  response['Access-Control-Allow-Origin']  = settings.RAPE_CORS_ORIGIN
			if settings.RAPE_CORS_METHODS: response['Access-Control-Allow-Methods'] = settings.RAPE_CORS_METHODS
			if settings.RAPE_CORS_HEADERS: response['Access-Control-Allow-Headers'] = settings.RAPE_CORS_HEADERS

			response['Content-Type'] = helpers.get_content_type(res_type)
			response['Cache-Control'] = 'public, max-age=86400'

			return response
		else: raise Http404
	else:
		return HttpResponseRedirect(reverse(('raped_%s' % res_type), args=(settings.RAPE_SERIAL, name)))


def generate_resource(request, res_type, name):
	print "Generating %s %s" % (res_type, name)
	output = helpers.get_output_path(request, res_type, name)
	file_list = helpers.get_file_list(res_type, name)

	if res_type == 'script': script.pack(request, file_list, output, settings.RAPE_PACK)
	elif res_type == 'style': style.pack(request, file_list, output, settings.RAPE_PACK)
	else: raise Exception('Unknown resource type: %s' % res_type)



