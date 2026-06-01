from sqlalchemy import create_engine, text
from sqlalchemy.pool import QueuePool
from flask import current_app
import pymysql

class DictCursorWrapper:
    """Wraps SQLAlchemy connection to behave like pymysql DictCursor."""
    def __init__(self, conn):
        self._conn = conn
        self._result = None

    def execute(self, query, args=None):
        if args:
            if isinstance(args, dict):
                # Named parameters - pass directly
                self._result = self._conn.execute(text(query), args)
            else:
                # Positional parameters - convert %s to :1, :2, :3, etc.
                param_list = list(args)
                converted_query = query
                for i in range(len(param_list)):
                    converted_query = converted_query.replace('%s', f':{i+1}', 1)
                bind_params = {str(i+1): v for i, v in enumerate(param_list)}
                self._result = self._conn.execute(text(converted_query), bind_params)
        else:
            self._result = self._conn.execute(text(query))

    def fetchone(self):
        if self._result:
            row = self._result.fetchone()
            return dict(row._mapping) if row else None
        return None

    def fetchall(self):
        if self._result:
            return [dict(row._mapping) for row in self._result.fetchall()]
        return []

    def __enter__(self):
        return self

    def __exit__(self, *args):
        pass

class SAConnection:
    """Wraps SQLAlchemy connection to behave like pymysql connection."""
    def __init__(self, conn):
        self._conn = conn

    def cursor(self):
        return DictCursorWrapper(self._conn)

    def commit(self):
        self._conn.commit()

    def rollback(self):
        self._conn.rollback()

    def close(self):
        self._conn.close()

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.close()

_engine = None

def get_engine(app):
    global _engine
    if _engine is None:
        host = app.config['MYSQL_HOST']
        port = app.config['MYSQL_PORT']
        user = app.config['MYSQL_USER']
        password = app.config['MYSQL_PASSWORD']
        database = app.config['MYSQL_DB']
        url = f"mysql+pymysql://{user}:{password}@{host}:{port}/{database}"
        _engine = create_engine(url, poolclass=QueuePool, pool_pre_ping=True, pool_recycle=300)
    return _engine

def get_db():
    engine = get_engine(current_app._get_current_object())
    conn = engine.connect()
    return SAConnection(conn)

def success_response(data=None, message="Success", status=200):
    return {"status": "success", "message": message, "data": data}, status

def error_response(message="Error", status=400):
    return {"status": "error", "message": message}, status

def success_response(data=None, message="Success", status=200):
    return {"status": "success", "message": message, "data": data}, status

def error_response(message="Error", status=400):
    return {"status": "error", "message": message}, status
