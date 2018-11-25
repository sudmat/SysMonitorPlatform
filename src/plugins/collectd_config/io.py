from jinja2 import Environment, FileSystemLoader

def write_to_config(config_info):
    file_loader = FileSystemLoader('templates')
    env = Environment(loader=file_loader)
    template = env.get_template('config')
    output = template.render(configs=config_info)
    return output

def read_from_config(config_str):
    return {}

if __name__ == '__main__':
    setting = {}
    setting['ReportByCpu'] = 'false'
    setting['ReportByState'] = 'true'
    setting['ValuesPercentage'] = 'false'

    cpu1 = {}
    cpu1['cpu1'] = setting

    setting = {}
    setting['ReportByCpu'] = 'false'
    setting['ReportByState'] = 'true'
    setting['ValuesPercentage'] = 'false'

    cpu2 = {}
    cpu2['cpu2'] = setting

    setting = {}
    setting['ReportByCpu'] = 'false'
    setting['ReportByState'] = 'true'
    setting['ValuesPercentage'] = 'false'

    cpu3 = {}
    cpu3['cpu3'] = setting

    config_list = [cpu1, cpu2, cpu3]

    x = write_to_config(config_list)
    print(x)

    y = read_from_config('')


