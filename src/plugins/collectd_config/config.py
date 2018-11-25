from collections import defaultdict

class CollectdConfig:

    def __init__(self, machine=''):
        self.machine = machine
        self.items = defaultdict(list)

    def add_item(self, meta_type, config_item):
        self.items[meta_type].append(config_item)

