from robocorp.tasks import task
from RPA.Database import Database
from RPA.Tables import Tables

database = Database()
tables = Tables()


def DB():
    conect_to_database()
    insert_into()
    database.disconnect_from_database()


def conect_to_database():
    database.connect_to_database(module_name='pymysql', database='prueba_db', username='root', host='localhost', port=3306)


def insert_into():
    robots = tables.read_table_from_csv(path='output/orders.csv')
    query_delete = 'TRUNCATE robot;'
    database.query(query_delete)
    for robot in robots:
        order_number = robot['Order number']
        head = robot['Head']
        body = robot['Body']
        legs = robot['Legs']
        address = robot['Address']
        query = f'INSERT INTO robot(order_number, head, body, legs, address) VALUES({order_number}, {head}, {body}, {legs}, "{address}")'
        database.query(statement=query)

def obtain_dat():
    conect_to_database()
    query = 'SELECT * FROM robot'
    dat = database.query(query)
    database.disconnect_from_database()
    return dat

