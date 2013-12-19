from StringIO import StringIO
from rape import helpers, settings
from scss import Scss

import os, os.path, shutil

def pack(file_list, output, minify=False):
	str_css = ""

	for res_name in file_list:
		fp = open(helpers.get_res_name('style', res_name), "r")
		str_css += helpers.replace_resource_urls(fp.read())
		fp.close()

	compiler = Scss()
	str_css = compiler.compile(str_css)

	#~ str_css = parser.loads()
	#~ print "%s" % str_css

	helpers.check_dir(os.path.dirname(output))
	ofp = open(output, "w+")
	ofp.write(str_css)
	ofp.close()



