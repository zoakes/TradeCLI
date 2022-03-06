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