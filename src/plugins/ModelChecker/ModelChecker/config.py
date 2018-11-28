from collections import defaultdict

class CollectdConfig:

    def __init__(self, file_name):
        self.file_name = file_name
        self.items = defaultdict(list)
        self.host = {}

    def set_host(self, host):
        self.host = host

    def add_item(self, meta_type, config_item):
        self.items[meta_type].append(config_item)

