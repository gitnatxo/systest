from ansible.vars import VariableManager
from ansible.inventory import Inventory as AnsibleInventory
from ansible.parsing.dataloader import DataLoader



import paramiko



class Group:

	def __init__(self, group_name, variables):

		self._name = group_name

		self._vars = variables

		self._hosts = dict()



	def __getitem__(self, key):

		return self._vars[key]



	def get_host(self, host_name):

		return self._hosts[host_name]



	def get_hosts(self):

		return self._hosts.values()



	def get_vars(self):

		return self._vars



class Host:

	def __init__(self, host_name, inventory):

		self._name = host_name

		self._inventory = inventory

		self._ssh = None




	def __getattr__(self, name):

		def method(*args):

			print("Plugin implementing mehod %s not found" % name)

			if args:

				print("It had arguments: " + str(args))

		return method



	def get_connection(self):

		if self._ssh == None:

			ssh = paramiko.SSHClient()

			ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

			pkey = paramiko.RSAKey.from_private_key(open(self.vars()['ansible_ssh_private_key_file'], 'r'))

			ssh.connect(self.vars()['ansible_host'], username = self.vars()['ansible_user'], pkey = pkey)

			self._ssh = ssh

		return self._ssh



	def do(self, command):

		ssh = self.get_connection()

		ins, out, err = ssh.exec_command(command)

		return out.readlines()



	def vars(self):

		return self._inventory.get_vars(self._name)



class Inventory:

	def __init__(self, source):

		self._source = source

		self._loader = DataLoader()

		self._variables = VariableManager()

		self._inventory = AnsibleInventory(loader = self._loader, variable_manager = self._variables, host_list = self._source)

		self._hosts = dict()

		self._groups = dict()



	def get_group(self, group_name):

		result = None

		if self._groups.has_key(group_name):

			result = self._groups[group_name]

		else:

			variables = self.get_group_vars(group_name)

			result = Group(group_name, variables)

			self._groups[group_name] = result

		return result



	def get_group_vars(self, group_name):

		result = None

		group = self._inventory.get_group(group_name)

		if group != None:

			result = self._inventory.get_group_vars(group)

		return result



	def get_host(self, host_name):

		result = None

		if self._hosts.has_key(host_name):

			result = self._hosts[host_name]

		else:

			host = self._inventory.get_host(host_name)

			if host != None:

				variables = self.get_vars(host_name)

				result = Host(host_name, self)

				self._hosts[host_name] = result

		return result



	def get_vars(self, host_name):

		result = None

		host = self._inventory.get_host(host_name)

		if host != None:

			result = self._variables.get_vars(self._loader, host = host)

		return result