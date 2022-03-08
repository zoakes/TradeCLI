SQL_USER = None
SQL_PASSWORD = None
SQL_IP = None


def set_sql_user(username):
    global SQL_USER
    SQL_USER = username

def set_sql_password(password):
    global SQL_PASSWORD
    SQL_PASSWORD = password

def set_sql_ip(ip):
    global SQL_IP
    SQL_IP = ip


def get_sql_ip():
    global SQL_IP
    return SQL_IP

def get_sql_user():
    global SQL_USER
    return SQL_USER

def get_sql_password():
    global SQL_PASSWORD
    return SQL_PASSWORD


def check_globals():
    global SQL_IP
    global SQL_PASSWORD
    global SQL_USER

    return SQL_IP, SQL_PASSWORD, SQL_USER






# ------------------ Refactor into dataclass with properties (or without -- simple statics) ---------------------------#
from dataclasses import dataclass

@dataclass
class Global:
    SQL_IP = None
    SQL_PASSWORD = None
    SQL_USER = None

    #For properties...



    # CAN define properties, but not needed?
    #  EXAMPLE var  /

    # _sql_ip = None
    #
    # @property
    # def SQL_IP(self):
    #     return self._sql_ip
    #
    # @SQL_IP.setter
    # def SQL_IP(self, value):
    #     self._sql_ip = value



# Global.SQL_IP = 1111111
# print(Global.SQL_IP)


