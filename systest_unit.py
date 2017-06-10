from inventory import Inventory

import sys
import unittest



inventory = None



class ReverseProxies(unittest.TestCase):

	def test_01_portal(self):

		host = inventory.get_host('intglabdb01')

		out = host.do('curl -i --insecure https://%s/check | egrep "^Server: " | sed -e "s/Server: //"' % inventory.get_host('intglabfe01').vars()['govlab_portal_server_name'])

		self.assertEqual(out[0], "Apache\r\n", "Failed to access web server")

		out = host.do('curl -i --insecure https://%s/portal-webapp/check | egrep "^Server: " | sed -e "s/Server: //"' % inventory.get_host('intglabfe01').vars()['govlab_portal_server_name'])

		self.assertEqual(out[0], "webapp\r\n", "Failed to proxy towards webapp")

	def test_02_back_office(self):

		host = inventory.get_host('intglabdb01')

		out = host.do('curl -i --insecure https://%s/check | egrep "^Server: " | sed -e "s/Server: //"' % inventory.get_host('intglabfe01').vars()['govlab_bo_server_name'])

		self.assertEqual(out[0], "Apache\r\n", "Failed to access web server")

		out = host.do('curl -i --insecure https://%s/bo-webapp/check | egrep "^Server: " | sed -e "s/Server: //"' % inventory.get_host('intglabfe01').vars()['govlab_bo_server_name'])

		self.assertEqual(out[0], "webapp\r\n", "Failed to proxy towards webapp")


if __name__ == '__main__':

	if len(sys.argv) > 1:

		inventory_source = sys.argv[1]

		del sys.argv[1]

		print inventory_source

		inventory = Inventory(inventory_source)

		unittest.main()