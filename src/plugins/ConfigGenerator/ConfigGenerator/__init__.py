"""
This is where the implementation of the plugin code goes.
The ConfigGenerator-class is imported from both run_plugin.py and run_debug.py
"""
import sys
import logging
from webgme_bindings import PluginBase
from collectd_config.config import CollectdConfig
from collectd_config.config_io import write_to_config

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
        core = self.core
        logger = self.logger
        # logger.debug('path: {0}'.format(core.get_path(active_node)))
        # logger.info('name: {0}'.format(core.get_attribute(active_node, 'name')))
        # logger.warn('pos : {0}'.format(core.get_registry(active_node, 'position')))
        # logger.error('guid: {0}'.format(core.get_guid(active_node)))
        # generate and save tree
        configs = self.get_config()
        config_content = configs[0].to_config()
        self.add_file('collectd.conf',config_content)
        # with open('collectd.conf', 'w') as f:
        #     f.write(config_content)

    def _get_collectd_config(self, monitor):
        config = CollectdConfig()
        for plugin in self.core.load_children(monitor):
            meta_node = self.core.get_meta_type(plugin)
            meta_type = self.core.get_attribute(meta_node, 'name')
            cur_item = {}
            for k in self.core.get_attribute_names(plugin):
                x = self.core.get_attribute(plugin, k)
                if k == 'name' or not x:
                    continue
                if isinstance(x, str):
                    x = '"' + x + '"'
                cur_item[k] = x
            config.add_item(meta_type, cur_item)
        return config

    def get_config(self):
        configs = []
        for machine in self.core.load_children(self.active_node):
            for monitor in self.core.load_children(machine):
                tool_type = self.core.get_attribute(monitor, 'tool')
                if tool_type == 'collectd':
                    cur_config = self._get_collectd_config(monitor)
                    configs.append(cur_config)
        return configs
