from inventory import Inventory

import paramiko

import sys



if __name__ == '__main__':

	if len(sys.argv) > 3:

		inventory_source = sys.argv[1]

		host_name = sys.argv[2]

		command = sys.argv[3]

		print 'Using inventory from source: %s' % inventory_source

		inventory = Inventory(inventory_source)

		host = inventory.get_host(host_name)

		print host.vars()

		stdout = host.do(command)

		print stdout.readlines()