from jinja2 import Environment, FileSystemLoader

def write_to_config(config_info):
    file_loader = FileSystemLoader('templates')
    env = Environment(loader=file_loader)
    template = env.get_template('config')
    output = template.render(configs=config_info)
    return output

def read_from_config(config_file):
    f = open(config_file, "r")
    dict_list = []

    # extract load
    load_plugin = {}
    for line in f.readlines():
        if line[0:10] == "LoadPlugin":
            load_name = line.split(" ")
            hardware_name = load_name[1].replace('\n', '')
            if "LoadPlugin" not in load_plugin:
                load_plugin["LoadPlugin"] = {}
                load_plugin["LoadPlugin"][hardware_name] = []
            else:
                load_plugin["LoadPlugin"][hardware_name] = []

    dict_list.append(load_plugin)
    f.close()

    # extract plugin
    f = open(config_file, "r")
    flag = False
    for line in f.readlines():
        if line[0:7] == "</Plugi" and flag:
            flag = False
            new_dict[hardware_name] = setting
            dict_list.append(new_dict)

        if flag:
            name_param = line.split(" ")
            setting_name = name_param[0].replace('\t', '')
            setting_param = name_param[1].replace('\n', '')
            if setting_name in setting:
                setting[setting_name].append(setting_param)
            else:
                setting[setting_name] = [setting_param]

        if line[0:7] == "<Plugin":
            flag = True
            hardware_name = ""
            n = 8
            while True:
                char = line[n]
                if char == ">":
                    break
                hardware_name += char
                n += 1
            # create a new dict for hardware to be monitored
            new_dict = {}
            setting = {}
    f.close()
    return dict_list

if __name__ == '__main__':

    y = read_from_config('collectd.conf')
    print(y)
    x = write_to_config(y)
    print(x)


