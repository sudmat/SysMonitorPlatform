from collections import Counter

def check_plugin_number(config):

    allowable = {
        'cpu': 1,
        'disk': -1,
        'interface': -1,
        'load': 1,
        'memory': 1,
        'rrdtool': 1,
        'csv': 1
    }
    violations = []
    for k, v in config.items.items():
        if k not in allowable:
            continue
        if allowable[k] != -1 and allowable[k] < len(v):
            violations.append('You cannot have more than %s %s '
                              'configuration in a single monitor'%(allowable[k], k))
    return violations

def check_os_compatibility(config):

    violations = []
    for item in config.items['disk']:
        if item.get('UseBSDName', False) and config.host['os_type'] != 'MacOS':
            violations.append('UseBSDName option should not be enabled on non-MacOS machine.')
            break

    return violations

def check_plugin_duplicity(config):

    violations = []
    disk_names = [item.get('Disk', '') for item in config.items['disk']]
    interface_names = [item.get('Interface', '') for item in config.items['interface']]

    disk_names_count = Counter(disk_names)
    interface_names_count = Counter(interface_names)

    for k, v in disk_names_count.items():
        if v >= 2:
            violations.append('Duplicated disk configuration with Disk= %s.'%k)

    for k, v in interface_names_count.items():
        if v >= 2:
            violations.append('Duplicated interface configuration with Disk= %s.'%k)

    return violations
