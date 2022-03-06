import configparser

CONFIG_PATH = None

def parse_config_file(path='C:\\Users\\zach\\PycharmProjects\\CLI\\CLILibTests\\cfg.txt', value='PASSWORD'):
    global CONFIG_PATH

    if CONFIG_PATH:
        path = CONFIG_PATH
        print('Using global CONFIG_PATH: ', CONFIG_PATH)
    else:
        CONFIG_PATH = path

    # print('CONFIG PATH: ', CONFIG_PATH) #Bingo !
    parser = configparser.ConfigParser()
    parser.read(path)

    parsed = parser.get('config', value)
    return parsed

#
# if not CONFIG_PATH:
#     CONFIG_PATH = 'C:\\Users\\zach\\PycharmProjects\\CLI\\CLILibTests\\cfg.txt'

# val = parse_config_file(value='PASSWORD')
# print(val)



# TRY adding logic here that parses OTHER vars, and SETS globals.globals ? #TODO