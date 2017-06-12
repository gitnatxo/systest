import re



def hook(caller, url):

	return URL(caller, url)



class URL:

	def __init__(self, caller, url):

		self._caller = caller

		self._url = url

		self._content = None



	def __repr__(self):

		return 'URL [%s]' % self._url



	def body(self):

		result = list()

		is_body = False

		for line in self.load():

			if not is_body:

				if len(line) == 0:

					is_body = True

			else:

				result.append(line)

		return result



	def header(self, header_name):

		result = None

		hs = self.headers(header_name)

		if len(hs) != 0:

			result = hs[0]

		return result



	def headers(self, header_name):

		header_pattern = re.compile('%s: (.*)' % header_name)

		return header_pattern.findall('\n'.join(self.load()))



	def load(self):

		if self._content == None:

			self._content = self._caller.do('curl -i --insecure %s' % self._url)

		return self._content



	def status(self):

		result = None

		status_pattern = re.compile('HTTP/... (...) .*')

		if self.load() != None and len(self.load()) > 0:

			status_match = status_pattern.findall(self.load()[0])

			if len(status_match) > 0:

				result = int(status_match[0])

		return result