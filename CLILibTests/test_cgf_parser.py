import configparser

parser = configparser.ConfigParser()

parser.read('cfg.txt') #CAN also use absolute path, I'm guessing?
pw = parser.get('config','PASSWORD')        # USE initial username + password as SQL USERNAME AND PASSWORD!
spw = parser.get('config','SQL_PASSWORD')
sun = parser.get('config','SQL_USER')
sip = parser.get('config','SQL_IP')

print(pw,spw,sun, sip)