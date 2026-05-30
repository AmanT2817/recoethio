import pymysql
from flask import current_app

def get_db():
    conn_params = {
        "host": current_app.config['MYSQL_HOST'],
        "user": current_app.config['MYSQL_USER'],
        "password": current_app.config['MYSQL_PASSWORD'],
        "database": current_app.config['MYSQL_DB'],
        "port": current_app.config['MYSQL_PORT'],
        "cursorclass": pymysql.cursors.DictCursor,
        "connect_timeout": 10,
        "read_timeout": 10,
        "write_timeout": 10
    }
    
    if current_app.config.get('MYSQL_SSL', False):
        conn_params['ssl_disabled'] = False
        conn_params['ssl_verify_cert'] = False
        conn_params['ssl_verify_identity'] = False
    
    conn = pymysql.connect(**conn_params)
    return conn

def success_response(data=None, message="Success", status=200):
    return {"status": "success", "message": message, "data": data}, status

def error_response(message="Error", status=400):
    return {"status": "error", "message": message}, status
