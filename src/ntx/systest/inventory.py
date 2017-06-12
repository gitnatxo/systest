from ansible.vars import VariableManager
from ansible.inventory import Inventory as AnsibleInventory
from ansible.parsing.dataloader import DataLoader



import functools
import importlib
import pkgutil



class Group:

    def __init__(self, group_name, inventory):
    
        self._name = group_name
        
        self._inventory = inventory
        
        self._hosts = dict()



    def __getitem__(self, name):

        return self.get(name)
        
        
        
    def get(self, name):
    
        result = None
       
        host = self.get_host(name)
       
        if host != None:
       
            result = host
           
        else:
           
            var = self._inventory.get_group_vars(self._name)[name]
               
            if var != None:
               
                result = var
                   
        return result
        
        
        
    def get_host(self, name):
    
        result = None
        
        if self._hosts.has_key(name):
        
            result = self._hosts[name]
            
        else:
        
            group_dict = self._inventory._inventory.get_group_dict()

            group = group_dict[self._name]

            if group != None:

                if name in group:

                    self._hosts[name] = self._inventory.get_host(name)

                    result = self._hosts[name]

        return result



class Host(object):

    _modules = None

    def __init__(self, host_name, inventory):
        
        self._name = host_name
        
        self._inventory = inventory
        
        self._ssh = None

        self.load_modules()



    def load_modules(self):

        if Host._modules == None:

            Host._modules = dict()

            for module_name in [name for _, name, _ in pkgutil.iter_modules(['modules'])]:

                module = importlib.import_module('modules.%s' % module_name)

                Host._modules[module_name] = module.hook
        
        
        
    def __getattr__(self, name):

        # TODO: look for module

        if Host._modules.has_key(name):

            p = functools.partial(Host._modules[name], self)

            return p

        else:

            return object.__getattribute__(self, name)



    def __getitem__(self, name):

        return self.get(name)
        
        
        
    def get(self, name):
    
        return self._inventory.get_host_vars(self._name)[name]
        
        
        
    def _get_connection(self):
    
        if self._ssh == None:
        
            ssh = paramiko.SSHClient()
            
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            
            pkey = paramiko.RSAKey.from_private_key(open(self['ansible_ssh_private_key_file'], 'r'))
            
            ssh.connect(self['ansible_host'], username = self['ansible_user'], pkey = pkey)
            
            self._ssh = ssh
            
        return self._ssh
        
        
        
    def do(self, command):
    
        ssh = self.get_connection()
        
        ins, out, err = ssh.exec_command(command)
        
        return out.readlines()



class Inventory:

    def __init__(self, source):
    
        self._source = source
        
        self._loader = DataLoader()
        
        self._variables = VariableManager()
        
        self._inventory = AnsibleInventory(loader = self._loader, variable_manager = self._variables, host_list = self._source)
        
        self._groups = dict()
        
        self._hosts = dict()



    def __getitem__(self, name):

        return self.get(name)
        
        
        
    def get(self, name):
    
        result = None
        
        host = self.get_host(name)
        
        if host != None:
        
            result = host
            
        else:
        
            group = self.get_group(name)
            
            if group != None:
            
                result = group
                
            else:
            
                group_all = self._inventory.get_group('all')
                
                if group_all != None:
                
                    var = group_all.get_vars()[name]
                    
                    if var != None:
                    
                        result = var
                        
        return result
        
        
        
    def get_group(self, group_name):
    
        result = None
        
        if self._groups.has_key(group_name):
        
            result = self._groups[group_name]
            
        elif self._inventory.get_group(group_name) != None:
        
            result = Group(group_name, self)
            
            self._groups[group_name] = result
            
        return result
        
        
        
    def get_group_vars(self, group_name):
    
        result = None
        
        group = self._inventory.get_group(group_name)
        
        if group != None:
        
            result = group.get_vars()
        
        return result
        
        
        
    def get_host(self, host_name):
    
        result = None
        
        if self._hosts.has_key(host_name):
        
            result = self._hosts[host_name]
            
        elif self._inventory.get_host(host_name) != None:
        
            result = Host(host_name, self)
            
            self._hosts[host_name] = result
            
        return result
        
        
        
    def get_host_vars(self, host_name):
    
        result = None
        
        host = self._inventory.get_host(host_name)
        
        if host != None:
        
            result = self._variables.get_vars(self._loader, host = host)
        
        return result



#------------------------------------------------------------------------------
# UNIT TESTING
#------------------------------------------------------------------------------



import unittest



class InvetoryTestCase(unittest.TestCase):

    def setUp(self):

        self.inventory = Inventory('unit_test.inv')



    def test_01_loading(self):

        self.assertNotEqual(None, self.inventory, 'Loading inventory')



    def test_02_inventory_hosts(self):

        self.assertEqual('localhost', self.inventory.get('localhost')._name, 'Reading host: localhost')

        self.assertEqual('localhost', self.inventory['localhost']._name, 'Reading host: localhost [getitem]')



    def test_03_inventory_groups(self):

        self.assertEqual('testing_group', self.inventory.get('testing_group')._name, 'Reading group: testing_group')

        self.assertEqual('testing_group', self.inventory['testing_group']._name, 'Reading group: testing_group [getitem]')



    def test_04_inventory_variables(self):

        self.assertEqual('bar_all', self.inventory.get('foo_all'), 'Reading an inventory-wide variable')

        self.assertEqual('bar_all', self.inventory['foo_all'], 'Reading an inventory-wide variable [getitem]')



    def test_05_group_hosts(self):

        group = self.inventory.get_group('testing_group')

        host = group.get('localhost')

        self.assertEqual('localhost', host._name, 'Reading host from group')

        self.assertEqual('localhost', group['localhost']._name, 'Reading host from group [getitem]')



    def test_06_group_variables(self):

        group = self.inventory.get_group('testing_group')

        self.assertEqual('bar', group.get('foo'), 'Reading a group var')

        self.assertEqual('bar', group['foo'], 'Reading a group var [getitem]')



    def test_07_host_variables(self):

        host = self.inventory.get_host('localhost')

        self.assertEqual('bar_all', host.get('foo_all'), 'Reading a host variable')

        self.assertEqual('bar_all', host['foo_all'], 'Reading a host variable [getitem]')



    def test_08_host_modules_hook(self):

        host = self.inventory.get_host('localhost')

        file = host.file('/tmp/foo.txt')

        self.assertEqual('File [/tmp/foo.txt]', file.__repr__(), 'Hooking modules from Host')



if __name__ == '__main__':

    unittest.main(verbosity = 2)