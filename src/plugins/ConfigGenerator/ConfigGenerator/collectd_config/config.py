from collections import defaultdict
from .config_io import write_to_config

class CollectdConfig:

    def __init__(self, file_name):
        self.file_name = file_name
        self.items = defaultdict(list)
        self.host = {}

    def set_host(self, host):
        self.host = host

    def add_item(self, meta_type, config_item):
        self.items[meta_type].append(config_item)

    def to_config(self):

        config_info = []
        for k, v in self.items.items():
            for section in v:
                attrs = {}
                for k0, v0 in section.items():
                    if isinstance(v0, bool):
                        v0 = 'true' if v0 else 'false'
                    attrs[k0] = [v0]
                config_info.append({k: attrs})

        config_content = write_to_config(config_info)
        return config_content

