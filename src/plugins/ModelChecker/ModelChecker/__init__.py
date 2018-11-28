"""
This is where the implementation of the plugin code goes.
The ModelChecker-class is imported from both run_plugin.py and run_debug.py
"""
import sys
import logging
from webgme_bindings import PluginBase
from .constraints import check_os_compatibility, check_plugin_duplicity, check_plugin_number
from .config import CollectdConfig

# Setup a logger
logger = logging.getLogger('ModelChecker')
logger.setLevel(logging.INFO)
handler = logging.StreamHandler(sys.stdout)  # By default it logs to stderr..
handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)


class ModelChecker(PluginBase):
    def main(self):

        cfg = self._get_collectd_config(self.active_node)
        violations = []
        violations += check_plugin_number(cfg)
        violations += check_plugin_duplicity(cfg)
        violations += check_os_compatibility(cfg)
        if violations:
            self.create_message(self.active_node, '</br>'.join(violations))
            raise RuntimeError()

    def _get_collectd_config(self, monitor):
        fn = self.core.get_attribute(monitor, 'cfg_file_name') \
             or self.core.get_attribute(monitor, 'name')
        cfg = CollectdConfig(file_name=fn)
        cfg.set_host({'os_type': self.core.get_attribute(monitor, 'os_type')})
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
            cfg.add_item(meta_type, cur_item)
        return cfg