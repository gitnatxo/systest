def hook(caller, path):

	return File(caller, path)



class File:

	def __init__(self, caller, path):

		self._caller = caller

		self._path = path



	def __repr__(self):

		return 'File [%s]' % self._path



	def cat(self):

		return self._caller.do('cat %s' % self._path)



	def head(self, n = 10):

		return self._caller.do('head -%d %s' % (n, self._path))



	def tail(self, n = 10):

		return self._caller.do('tail -%d %s' % (n, self._path))