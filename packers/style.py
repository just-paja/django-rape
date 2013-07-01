from StringIO import StringIO
from rape import helpers, settings
from scss.parser import Stylesheet

import os, os.path, shutil

def pack(file_list, output, minify=False):
	str_css = ""

	for res_name in file_list:
		fp = open(helpers.get_res_name('style', res_name), "r")
		str_css += helpers.replace_resource_urls(fp.read())
		fp.close()

	parser = Stylesheet(options = {
		"compress":settings.RAPE_PACK
	})

	str_css = parser.loads(str_css)
	#~ print "%s" % str_css

	ofp = open(output, "w+")
	ofp.write(str_css)
	ofp.close()



