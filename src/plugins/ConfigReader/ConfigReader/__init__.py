"""
This is where the implementation of the plugin code goes.
The ConfigReader-class is imported from both run_plugin.py and run_debug.py
"""
import sys
import logging
from webgme_bindings import PluginBase

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

        meta = self._get_meta()
        memory = self.core.create_child(self.active_node, meta['memory'])
        self.core.create_node({'base': meta['memory']})
        # self.core.set_attribute(monitor, 'name', 'test')
        print(1)

    def _get_meta(self):

        nodes_mapping = {}
        root = self.core.get_root(self.active_node)
        for c in self.core.load_children(root):
            if not self.core.is_meta_node(c):
                continue
            name = self.core.get_attribute(c, 'name')
            nodes_mapping[name] = c

        return nodes_mapping
