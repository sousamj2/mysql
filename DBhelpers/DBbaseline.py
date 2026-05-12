from flask import current_app
import pymysql
import sys
import os

def get_mysql_connection(use_dict_cursor: bool = False):
    """
    Establishes and returns a connection to the MySQL database.

    This function retrieves database connection parameters (host, database name, user,
    password, port) from the current Flask application's configuration. It then
    uses these parameters to create and return a `pymysql` connection object.

    Args:
        use_dict_cursor (bool, optional): If True, the connection's cursor will
            return rows as dictionaries instead of the default tuples.
            Defaults to False.

    Returns:
        pymysql.Connection | None: A `pymysql` connection object on success, or
        `None` if the connection fails.
    """
    # Load from env vars or AWS Secrets/Parameter Store
    MYSQL_HOST = current_app.config['MYSQL_HOST']
    # MYSQL_HOST = "localhost"
    MYSQL_NAME = current_app.config['MYSQL_DBNAME']
    MYSQL_USER = current_app.config['MYSQL_USER']
    MYSQL_PASS = current_app.config['MYSQL_PASSWORD']
    MYSQL_PORT = int(current_app.config['MYSQL_PORT'])
    # MYSQL_PORT = 3307

    cursor_cls = pymysql.cursors.DictCursor if use_dict_cursor else pymysql.cursors.Cursor

    try:
        conn = pymysql.connect(
            host=MYSQL_HOST,
            port=MYSQL_PORT,
            db=MYSQL_NAME,
            user=MYSQL_USER,
            password=MYSQL_PASS,
            charset="utf8mb4",
            cursorclass=cursor_cls,
            use_unicode=True,
            )
        return conn
    except Exception as e:
        print(f"Error connecting: {e}")
        return None


def setup_mysql_database(app_name: str = "mc_mjcrafts"):
    """
    Initializes the application's database schema.
    """
    import importlib.util
    
    # Dynamically import the config based on app_name
    if app_name == "explicolivais":
        config_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../explicolivais/config.py'))
    else:
        config_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../simplewebapp/config.py'))
        
    spec = importlib.util.spec_from_file_location("dynamic_config", config_path)
    config_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(config_module)
    DevelopmentConfig = config_module.DevelopmentConfig

    MYSQL_HOST = DevelopmentConfig.MYSQL_HOST or ""
    MYSQL_NAME = DevelopmentConfig.MYSQL_DBNAME or ""
    MYSQL_USER = DevelopmentConfig.MYSQL_USER or ""
    MYSQL_PASS = DevelopmentConfig.MYSQL_PASSWORD or ""
    MYSQL_PORT = DevelopmentConfig.MYSQL_PORT or ""

    # Connect to MySQL server (without specifying database)
    conn = pymysql.connect (
        host=MYSQL_HOST,
        user=MYSQL_USER,
        password=MYSQL_PASS,
        port=MYSQL_PORT,
        charset="utf8mb4",
        cursorclass=pymysql.cursors.Cursor,
        autocommit=True,
        use_unicode=True,
    )
    cursor = conn.cursor()
        
    from . import (
        newTableResults,
        newTableConnectionData,
        newTableIPs,
        newTableUsers,
        newTableBlacklistEmails,
        newTableBlacklistIPs,
        newTableRegistrationTokens,
        newTableClass,
        newTableDocuments,
        newTablePersonalData,
    )

    try:
        # Create database if it doesn't exist
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {MYSQL_NAME}")
        # Switch to the database
        cursor.execute(f"USE {MYSQL_NAME}")
        
        newTableUsers(cursor, app_name)
        newTableConnectionData(cursor, app_name)
        newTableIPs(cursor, app_name)
        newTableResults(cursor, app_name)
        newTableBlacklistEmails(cursor)
        newTableBlacklistIPs(cursor)
        newTableRegistrationTokens(cursor)
        
        if app_name == "explicolivais":
            newTableClass(cursor)
            newTableDocuments(cursor)
            newTablePersonalData(cursor)
        
        print("Database setup completed successfully!", flush=True)
                
    except Exception as err:
        print(f"Error: {err}")
    
    finally:
        cursor.close()
        conn.close()
