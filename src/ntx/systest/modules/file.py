def hook(caller, path):

	return File(caller, path)



class File:

	def __init__(self, caller, path):

		self._caller = caller

		self._path = path



	def __repr__(self):

		return 'File [%s]' % self._path