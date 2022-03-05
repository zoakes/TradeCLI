
# ---------------------------------------- SQL METHODS --------------------------------------------------- ##
import mysql.connector
import asyncio
import datetime

from cfg import SQL_PASSWORD, SQL_USER

cnx = None
cur = None


def sql_init():
    global cnx
    global cur

    cnx = mysql.connector.connect(user=SQL_USER, password=SQL_PASSWORD,
                                  host = '192.168.1.178',
                                  database='test',
                                  auth_plugin='mysql_native_password',
                                  autocommit=True)
    cur = cnx.cursor(buffered=True)


def get_orders(sent=None, filled=None):
    global cnx
    global cur

    if cnx is None or cur is None:
        sql_init()

    if sent != None:
        _sent = 1 if sent else 0

    if filled != None:
        _filled = 1 if filled else 0

    #IF selection made for both...
    if sent and filled:
        cur.execute(f"SELECT * FROM oms WHERE sent = {_sent} AND filled = {_filled}")

    if sent and not filled:
        cur.execute(f"SELECT * FROM oms WHERE sent = {_sent}")

    if filled and not sent:
        cur.execute(f"SELECT * FROM oms WHERE filled = {_sent}")

    if not filled and not sent:
        cur.execute(f'SELECT * from oms')

    results = cur.fetchall()
    return results


def get_all_orders():
    global cnx
    global cur

    if cnx is None or cur is None:
        sql_init()

    cur.execute("SELECT * FROM oms")
    results = cur.fetchall()
    return results

def get_all_unsent():
    global cnx
    global cur

    if cnx is None or cur is None:
        sql_init()

    cur.execute("SELECT * FROM oms WHERE sent = 0")
    results = cur.fetchall()
    return results


def get_all_unfilled():
    global cnx
    global cur

    if cnx is None or cur is None:
        sql_init()

    cur.execute("SELECT * FROM oms WHERE filled = 0")
    results = cur.fetchall()
    return results


def get_all_pending():
    global cnx
    global cur

    if cnx is None or cur is None:
        sql_init()

    cur.execute("SELECT * FROM oms WHERE sent = 1 AND filled = 0")
    results = cur.fetchall()
    return results

def get_all_filled():
    global cnx
    global cur

    if cnx is None or cur is None:
        sql_init()

    cur.execute("SELECT * FROM oms WHERE filled = 1")
    results = cur.fetchall()
    return results


def sql_update_sent(uid):
    global cnx
    global cur

    sql = f"UPDATE oms SET sent = 1 WHERE uid = {uid}"  # ?"  # (%s)"
    cur.execute(sql)
    cnx.commit()


# ----------------------- OLD Async versions -------------------- ##
'''

async def sql_init():
    global cnx
    global cur

    cnx = mysql.connector.connect(user='zach', password='zoakes1290',
                                  host = '192.168.1.178',
                                  database='test',
                                  auth_plugin='mysql_native_password',
                                  autocommit=True)
    cur = cnx.cursor(buffered=True)



async def read_sql():
    # SAVEd credentials (MOVE to config)
    # https://stackoverflow.com/questions/9305669/mysql-python-connection-does-not-see-changes-to-database-made-on-another-connect
    global cnx
    global cur

    if cnx is None or cur is None:
        await sql_init()

    cur.execute("SELECT * FROM oms WHERE sent = 0")                                                                     # SET THIS IN CFG_?
    results = cur.fetchall()
    return results


def sql_update_filled(symbol, side, qty):
    """
    Since it doesnt matter WHICH order is filled (in case of 2x identical MKT orders)...
    WHY not simply report the FIRST one (not filled) as FILLED.
    :param symbol: Symbol filled (root or front?), STR
    :param side: 1 or -1, INT
    :param qty: 1 - 100, INT
    :return: None
    """

    global cnx
    global cur
    global filled
    #global last_uid    # Maybe this is better ?

    try:
        root = symbol[0:2] # ENSURE this uses ROOT and not SYMBOL here !!
        sent_not_filled = [i for i in sent if i not in filled]
        approx_uid = [i[0] for i in sent_not_filled if i[1] == root and i[2] == side and i[3] == qty]

        sql = f"UPDATE oms SET filled = 1 WHERE uid = {approx_uid}"

        cur.execute(sql)
        cnx.commit()
        print(f'Order Filled {root, side, qty}')
        return 1
    except Exception as e:
        print("Failed fill update-- ", e)
        return -1


async def kill_sql_task():
    #https://stackoverflow.com/questions/44982332/asyncio-await-and-infinite-loops
    global g_sql_task

    task = g_sql_task

    task.cancel()
    with suppress(asyncio.CancelledError):
        await task  # await for task cancellation

'''



