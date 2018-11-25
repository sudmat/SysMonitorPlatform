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
    return dict_list

if __name__ == '__main__':
    setting = {}
    setting['ReportByCpu'] = ['false']
    setting['ReportByState'] = ['true']
    setting['ValuesPercentage'] = ['false']

    cpu1 = {}
    cpu1['cpu1'] = setting

    setting = {}
    setting['ReportByCpu'] = ['false', 'false', 'true']
    setting['ReportByState'] = ['true']
    setting['ValuesPercentage'] = ['false']

    cpu2 = {}
    cpu2['cpu2'] = setting

    setting = {}
    setting['ReportByCpu'] = ['false']
    setting['ReportByState'] = ['true']
    setting['ValuesPercentage'] = ['false']

    cpu3 = {}
    cpu3['cpu1'] = setting

    config_list = [cpu1, cpu2, cpu3]

    x = write_to_config(config_list)
    #print(x)

    y = read_from_config('collectd.conf')
    print(y)


