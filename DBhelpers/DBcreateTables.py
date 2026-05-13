import os
createFolder = os.path.join(os.path.dirname(__file__), "..", "MySQLqueries", "createHandler", "")

def create_tables(sql_file_path,cursor):
    """
    Executes a CREATE TABLE SQL script from a file.

    This function reads an SQL file containing a `CREATE TABLE` statement and
    executes it using the provided database cursor. It is a generic utility
    used by other functions to create specific tables.

    Args:
        sql_file_path (str): The path to the .sql file containing the CREATE TABLE command.
        cursor (pymysql.cursors.Cursor): The database cursor to use for executing the command.

    Returns:
        str: A status message indicating whether the table was created successfully
             or if an error occurred.
    """

    try:
        # Read SQL code from file
        with open(sql_file_path, 'r') as file:
            sql_code = file.read()

        # Execute the SQL command
        cursor.execute(sql_code)

        status = "Table created successfully"
    except Exception as e:
        status = f"Error creating table: {e} from {sql_file_path}"
        # print(status)

    return status


def newTableIPs(cursor, app_name="mc_mjcrafts"):
    """
    Creates the 'iplist' table in the database.
    """
    if app_name == "explicolivais":
        sql_file = "create_iplist.sql"
    else:
        sql_file = "create_iplist_simplewebapp.sql"
    return create_tables(sql_file_path=createFolder + sql_file, cursor=cursor)

def newTableResults(cursor, app_name="mc_mjcrafts"):
    """
    Creates the 'qresults' table in the database.
    """
    if app_name == "explicolivais":
        sql_file = "create_qresults.sql"
    else:
        sql_file = "create_qresults_simplewebapp.sql"
    return create_tables(sql_file_path=createFolder + sql_file, cursor=cursor)


def newTableConnectionData(cursor, app_name="mc_mjcrafts"):
    """
    Creates the 'connections' table in the database.
    """
    if app_name == "explicolivais":
        sql_file = "create_connections.sql"
    else:
        sql_file = "create_connections_simplewebapp.sql"
    return create_tables(sql_file_path=createFolder + sql_file, cursor=cursor)


def newTableUsers(cursor, app_name="mc_mjcrafts"):
    """
    Creates the 'users' table in the database.

    This function calls the generic `create_tables` utility to execute the
    SQL script for creating the `users` table.

    Args:
        cursor (pymysql.cursors.Cursor): The database cursor to use.
        app_name (str): The name of the application to determine the correct schema.
    """
    if app_name == "explicolivais":
        sql_file = "create_users_explicolivais.sql"
    else:
        sql_file = "create_users_simplewebapp.sql"
    
    return create_tables(sql_file_path=createFolder + sql_file, cursor=cursor)

def newTableBlacklistEmails(cursor):
    """
    Creates the 'blacklist_emails' table in the database.
    
    This function calls the generic `create_tables` utility to execute the
    SQL script for creating the `blacklist_emails` table.

    Args:
        cursor (pymysql.cursors.Cursor): The database cursor to use.
    """
    return create_tables(sql_file_path=createFolder + "create_blacklist_emails.sql",cursor=cursor)

def newTableBlacklistIPs(cursor):
    """
    Creates the 'blacklist_ips' table in the database.
    
    This function calls the generic `create_tables` utility to execute the
    SQL script for creating the `blacklist_ips` table.

    Args:
        cursor (pymysql.cursors.Cursor): The database cursor to use.
    """
    return create_tables(sql_file_path=createFolder + "create_blacklist_ips.sql",cursor=cursor)

def newTableRegistrationTokens(cursor):
    """
    Creates the 'registration_tokens' table in the database.
    
    This function calls the generic `create_tables` utility to execute the
    SQL script for creating the `registration_tokens` table.

    Args:
        cursor (pymysql.cursors.Cursor): The database cursor to use.
    """
    return create_tables(sql_file_path=createFolder + "create_registration_tokens.sql",cursor=cursor)

def newTableClass(cursor):
    """
    Creates the 'classes' table in the database.
    """
    return create_tables(sql_file_path=createFolder + "create_classes.sql",cursor=cursor)

def newTableDocuments(cursor):
    """
    Creates the 'documents' table in the database.
    """
    return create_tables(sql_file_path=createFolder + "create_documents.sql",cursor=cursor)

def newTablePersonalData(cursor):
    """
    Creates the 'personal' table in the database.
    """
    return create_tables(sql_file_path=createFolder + "create_personal.sql",cursor=cursor)
