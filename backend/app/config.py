import os
from datetime import timedelta
from urllib.parse import urlparse

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY', 'jwt-secret-key-change-in-production')
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=24)

    # Parse Railway database URL if available
    mysql_url = (
        os.environ.get('MYSQL_PUBLIC_URL')
        or os.environ.get('MYSQL_URL')
        or os.environ.get('DATABASE_URL')
        or ''
    )

    if mysql_url:
        parsed = urlparse(mysql_url)
        MYSQL_HOST = parsed.hostname or 'localhost'
        MYSQL_PORT = parsed.port or 3306
        MYSQL_USER = parsed.username or 'root'
        MYSQL_PASSWORD = parsed.password or ''
        MYSQL_DB = parsed.path.lstrip('/') or 'recommendation_system'
    else:
        MYSQL_HOST = os.environ.get('MYSQLHOST', 'localhost')
        MYSQL_PORT = int(os.environ.get('MYSQLPORT', 3306))
        MYSQL_USER = os.environ.get('MYSQLUSER', 'root')
        MYSQL_PASSWORD = os.environ.get('MYSQLPASSWORD', '')
        MYSQL_DB = os.environ.get('MYSQLDATABASE', 'recommendation_system')

    MYSQL_SSL = (
        os.environ.get('MYSQL_SSL', '').lower() in ('1', 'true', 'yes')
        or 'ballast' in MYSQL_HOST
    )
