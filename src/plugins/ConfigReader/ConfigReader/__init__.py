"""
This is where the implementation of the plugin code goes.
The ConfigReader-class is imported from both run_plugin.py and run_debug.py
"""
import sys
import logging
from webgme_bindings import PluginBase
from .config_io import read_from_config
from collections import Counter

# Setup a logger
logger = logging.getLogger('ConfigReader')
logger.setLevel(logging.INFO)
handler = logging.StreamHandler(sys.stdout)  # By default it logs to stderr..
handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)


class ConfigReader(PluginBase):
    def main(self):
        core = self.core
        root_node = self.root_node
        active_node = self.active_node
        self.save_file()
        proj_node = self.core.get_parent(active_node)
        self.proj_node = proj_node
        config_content = read_from_config(self._temp_file_name())
        self.add_config2model(config_content)
        # logger.info(x)

    @staticmethod
    def _temp_file_name():
        return __file__.replace('__init__.py', 'uploaded/test.conf')

    def save_file(self):
        cc = self.get_current_config()
        file_content = self.get_file(cc['configuration'])
        with open(self._temp_file_name(), 'w') as f:
            f.write(file_content)

    def add_config2model(self, config_info):
        meta = self._get_meta()
        nbr = self._get_monitor_nbr()
        monitor = self.core.create_child(self.active_node, meta['Monitor'])
        monitor_name = 'CollectdMonitor%s'%(nbr+1)
        self.core.set_attribute(monitor, 'name', monitor_name)
        tmp = []
        unknown_plugin = []
        for item in config_info:
            tmp += list(item)
        plugin_nbr = Counter(tmp)
        for item in config_info:
            for k, v in item.items():
                if k not in meta:
                    unknown_plugin.append(k)
                    continue
                if plugin_nbr[k] <= 1:
                    plugin_name = k
                else:
                    plugin_name = k+str(plugin_nbr[k])
                    plugin_nbr[k] -= 1
                plugin = self.core.create_child(monitor, meta[k])
                for attr, values in v.items():
                    for value in values:
                        value = value.replace('"', '')
                        if value == 'true':
                            value = True
                        if value == 'false':
                            value = False
                        self.core.set_attribute(plugin, attr, value)
                self.core.set_attribute(plugin, 'name', plugin_name)
        if unknown_plugin:
            self.create_message(self.active_node, 'unrecognozied plugin(s): %s'%', '.join(unknown_plugin))
        self.util.save(self.root_node, self.commit_hash, 'master', 'Monitor Added name=%s'%monitor_name)

    def _get_monitor_nbr(self):
        count = len(self.core.load_children(self.active_node))
        return count

    def _get_meta(self):

        nodes_mapping = {}
        root = self.core.get_root(self.active_node)
        for c in self.core.load_children(root):
            if not self.core.is_meta_node(c):
                continue
            name = self.core.get_attribute(c, 'name')
            nodes_mapping[name] = c

        return nodes_mapping
