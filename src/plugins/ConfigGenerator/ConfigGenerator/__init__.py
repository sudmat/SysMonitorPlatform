"""
This is where the implementation of the plugin code goes.
The ConfigGenerator-class is imported from both run_plugin.py and run_debug.py
"""
import sys
import logging
from webgme_bindings import PluginBase

from .collectd_config.config import CollectdConfig

# Setup a logger
logger = logging.getLogger('ConfigGenerator')
logger.setLevel(logging.INFO)
handler = logging.StreamHandler(sys.stdout)  # By default it logs to stderr..
handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)


class ConfigGenerator(PluginBase):
    def main(self):
        active_node = self.active_node
        proj_node = self.core.get_parent(active_node)
        self.proj_node = proj_node
        x = self.get_current_config()
        configs = self.get_config()
        for cfg in configs:
            config_content = cfg.to_config()
            self.add_file('%s.conf'%cfg.file_name,config_content)

    def _get_collectd_config(self, monitor):
        fn = self.core.get_attribute(monitor, 'cfg_file_name') \
             or self.core.get_attribute(monitor, 'name')
        config = CollectdConfig(file_name=fn)
        for plugin in self.core.load_children(monitor):
            meta_node = self.core.get_meta_type(plugin)
            meta_type = self.core.get_attribute(meta_node, 'name')
            cur_item = {}
            for k in self.core.get_attribute_names(plugin):
                x = self.core.get_attribute(plugin, k)
                if k == 'name' or x == '':
                    continue
                if isinstance(x, str):
                    x = '"' + x + '"'
                cur_item[k] = x
            config.add_item(meta_type, cur_item)
        return config

    def get_config(self):
        configs = []
        for monitor in self._get_monitor_nodes():
            tool_type = self.core.get_attribute(monitor, 'tool')
            if tool_type == 'collectd':
                cur_config = self._get_collectd_config(monitor)
                configs.append(cur_config)
        return configs

    def _get_monitor_nodes(self):
        monitors = self.core.load_children(self.active_node)
        return monitors



