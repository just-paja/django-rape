from StringIO import StringIO
from rape import helpers, settings
import os, os.path, shutil


def pack(file_list, output, minify=False):
	str_js = ""

	for res_name in file_list:
		fp = open(helpers.get_res_name('script', res_name), "r")
		str_js += helpers.replace_resource_urls(fp.read())
		fp.close()

	if settings.RAPE_PACK:
		str_js = jsmin(str_js)

	ofp = open(output, "w+")
	ofp.write(str_js)
	ofp.close()


def jsmin(js):
	ins = StringIO(js)
	outs = StringIO()
	JavascriptMinify().minify(ins, outs)
	str = outs.getvalue()
	if len(str) > 0 and str[0] == '\n':
		str = str[1:]
	return str


def isAlphanum(c):
	"""return true if the character is a letter, digit, underscore,
		   dollar sign, or non-ASCII character.
	"""
	return ((c >= 'a' and c <= 'z') or (c >= '0' and c <= '9') or
			(c >= 'A' and c <= 'Z') or c == '_' or c == '$' or c == '\\' or (c is not None and ord(c) > 126));

class UnterminatedComment(Exception):
	pass

class UnterminatedStringLiteral(Exception):
	pass

class UnterminatedRegularExpression(Exception):
	pass

class JavascriptMinify(object):

	def _outA(self):
		self.outstream.write(self.theA)
	def _outB(self):
		self.outstream.write(self.theB)

	def _get(self):
		"""return the next character from stdin. Watch out for lookahead. If
		   the character is a control character, translate it to a space or
		   linefeed.
		"""
		c = self.theLookahead
		self.theLookahead = None
		if c == None:
			c = self.instream.read(1)
		if c >= ' ' or c == '\n':
			return c
		if c == '': # EOF
			return '\000'
		if c == '\r':
			return '\n'
		return ' '

	def _peek(self):
		self.theLookahead = self._get()
		return self.theLookahead

	def _next(self):
		"""get the next character, excluding comments. peek() is used to see
		   if an unescaped '/' is followed by a '/' or '*'.
		"""
		c = self._get()
		if c == '/' and self.theA != '\\':
			p = self._peek()
			if p == '/':
				c = self._get()
				while c > '\n':
					c = self._get()
				return c
			if p == '*':
				c = self._get()
				while 1:
					c = self._get()
					if c == '*':
						if self._peek() == '/':
							self._get()
							return ' '
					if c == '\000':
						raise UnterminatedComment()

		return c

	def _action(self, action):
		"""do something! What you do is determined by the argument:
		   1   Output A. Copy B to A. Get the next B.
		   2   Copy B to A. Get the next B. (Delete A).
		   3   Get the next B. (Delete B).
		   action treats a string as a single character. Wow!
		   action recognizes a regular expression if it is preceded by ( or , or =.
		"""
		if action <= 1:
			self._outA()

		if action <= 2:
			self.theA = self.theB
			if self.theA == "'" or self.theA == '"':
				while 1:
					self._outA()
					self.theA = self._get()
					if self.theA == self.theB:
						break
					if self.theA <= '\n':
						raise UnterminatedStringLiteral()
					if self.theA == '\\':
						self._outA()
						self.theA = self._get()


		if action <= 3:
			self.theB = self._next()
			if self.theB == '/' and (self.theA == '(' or self.theA == ',' or
									 self.theA == '=' or self.theA == ':' or
									 self.theA == '[' or self.theA == '?' or
									 self.theA == '!' or self.theA == '&' or
									 self.theA == '|' or self.theA == ';' or
									 self.theA == '{' or self.theA == '}' or
									 self.theA == '\n'):
				self._outA()
				self._outB()
				while 1:
					self.theA = self._get()
					if self.theA == '/':
						break
					elif self.theA == '\\':
						self._outA()
						self.theA = self._get()
					elif self.theA <= '\n':
						raise UnterminatedRegularExpression()
					self._outA()
				self.theB = self._next()


	def _jsmin(self):
		"""Copy the input to the output, deleting the characters which are
		   insignificant to JavaScript. Comments will be removed. Tabs will be
		   replaced with spaces. Carriage returns will be replaced with linefeeds.
		   Most spaces and linefeeds will be removed.
		"""
		self.theA = '\n'
		self._action(3)

		while self.theA != '\000':
			if self.theA == ' ':
				if isAlphanum(self.theB):
					self._action(1)
				else:
					self._action(2)
			elif self.theA == '\n':
				if self.theB in ['{', '[', '(', '+', '-']:
					self._action(1)
				elif self.theB == ' ':
					self._action(3)
				else:
					if isAlphanum(self.theB):
						self._action(1)
					else:
						self._action(2)
			else:
				if self.theB == ' ':
					if isAlphanum(self.theA):
						self._action(1)
					else:
						self._action(3)
				elif self.theB == '\n':
					if self.theA in ['}', ']', ')', '+', '-', '"', '\'']:
						self._action(1)
					else:
						if isAlphanum(self.theA):
							self._action(1)
						else:
							self._action(3)
				else:
					self._action(1)

	def minify(self, instream, outstream):
		self.instream = instream
		self.outstream = outstream
		self.theA = '\n'
		self.theB = None
		self.theLookahead = None

		self._jsmin()
		self.instream.close()

def compress(in_files, out_file, in_type='js', verbose=False,
			 temp_file='.temp'):
	temp = open(temp_file, 'w')
	for f in in_files:
		fh = open(f)
		data = fh.read() + '\n'
		fh.close()

		temp.write(data)

		print ' + %s' % f
	temp.close()

	out = open(out_file, 'w')

	jsm = JavascriptMinify()
	jsm.minify(open(temp_file,'r'), out)

	out.close()

	org_size = os.path.getsize(temp_file)
	new_size = os.path.getsize(out_file)

	print '=> %s' % out_file
	print 'Original: %.2f kB' % (org_size / 1024.0)
	print 'Compressed: %.2f kB' % (new_size / 1024.0)
	print 'Reduction: %.1f%%' % (float(org_size - new_size) / org_size * 100)
	print ''

	os.remove(temp_file)