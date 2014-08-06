from StringIO import StringIO
from rape import helpers, settings
import os, os.path, shutil, json, uglipyjs


def pack(request, file_list, output, minify=False):
	str_js = ""

	if not settings.RAPE_PACK:
		str_js = "/* File list:\n%s\n*/\n\n" % json.dumps(file_list, indent=4, sort_keys=True)

	for res_name in file_list:
		fp = open(res_name, "r")
		str_js += helpers.replace_resource_urls(request, fp.read())
		fp.close()

	if settings.RAPE_PACK:
		str_js = uglipyjs.compile(str_js)

	helpers.check_dir(os.path.dirname(output))
	ofp = open(output, "w+")
	ofp.write(str_js)
	ofp.close()
