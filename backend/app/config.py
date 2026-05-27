import os
from datetime import timedelta

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY', 'jwt-secret-key-change-in-production')
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=24)

    MYSQL_HOST     = os.environ.get('MYSQLHOST', 'localhost')
    MYSQL_USER     = os.environ.get('MYSQLUSER', 'root')
    MYSQL_PASSWORD = os.environ.get('MYSQLPASSWORD', '')
    MYSQL_DB       = os.environ.get('MYSQLDATABASE', 'recommendation_system')
    MYSQL_PORT     = int(os.environ.get('MYSQLPORT', 3306))
