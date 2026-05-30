import pymysql
import pymysql.cursors
from flask import current_app

def get_db():
    host = current_app.config['MYSQL_HOST']
    port = current_app.config['MYSQL_PORT']
    user = current_app.config['MYSQL_USER']
    password = current_app.config['MYSQL_PASSWORD']
    database = current_app.config['MYSQL_DB']

    # Use URL-based connection for Railway compatibility
    conn = pymysql.connect(
        host=host,
        user=user,
        password=password,
        database=database,
        port=int(port),
        cursorclass=pymysql.cursors.DictCursor,
        connect_timeout=10,
        read_timeout=10,
        write_timeout=10,
        ssl={'ca': None, 'check_hostname': False, 'verify_mode': 0}
    )
    return conn

def success_response(data=None, message="Success", status=200):
    return {"status": "success", "message": message, "data": data}, status

def error_response(message="Error", status=400):
    return {"status": "error", "message": message}, status
