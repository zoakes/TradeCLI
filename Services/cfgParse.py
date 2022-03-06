import configparser

CONFIG_PATH = None

def parse_config_file(path='C:\\Users\\zach\\PycharmProjects\\CLI\\CLILibTests\\cfg.txt', value='PASSWORD'):
    global CONFIG_PATH

    if CONFIG_PATH:
        path = CONFIG_PATH

    parser = configparser.ConfigParser()
    parser.read(path)

    parsed = parser.get('config', value)
    return parsed

#
# if not CONFIG_PATH:
#     CONFIG_PATH = 'C:\\Users\\zach\\PycharmProjects\\CLI\\CLILibTests\\cfg.txt'

# val = parse_config_file(value='PASSWORD')
# print(val)