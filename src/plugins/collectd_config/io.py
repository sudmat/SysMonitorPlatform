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

    x = write_to_config({})

    y = read_from_config('')


