import json
from uuid import uuid4
from datetime import datetime # Import datetime
from .DBselectTables import getUserIdFromEmail
import os
insertFolder = os.path.join(os.path.dirname(__file__), "..", "MySQLqueries", "insertHandler", "")

from .DBbaseline import get_mysql_connection

def execute_insert_from_file(sql_file_path, params_dict):
    """
    Executes a parameterized INSERT query from an SQL file.

    This function reads an SQL INSERT statement from a file, connects to the
    MySQL database, and executes the query using a dictionary of parameters.
    The function replaces '?' placeholders in the SQL file with '%s' to ensure
    compatibility with `pymysql`. The connection is automatically opened and
    closed.

    Args:
        sql_file_path (str): The path to the .sql file containing the INSERT statement.
        params_dict (dict): A dictionary where keys correspond to the data fields
                            and values are the data to be inserted. The order of
                            items in the dictionary is assumed to match the order
                            of placeholders in the SQL query.

    Returns:
        str: A status message indicating the success or failure of the insert operation.
    """
    # print(sql_file_path)

    try:
        # Read SQL code from file
        with open(sql_file_path, "r") as file:
            sql_code = file.read()

            # print(sql_code.replace("?","%s"))

        # Connect to database
        conn = get_mysql_connection()
        if not conn:
            raise ConnectionError("Could not connect to MySQL database")

        cursor = conn.cursor()

        # Prepare parameters tuple in the order matching the SQL placeholders
        # Assuming params_dict is an OrderedDict or that order is known
        params = tuple(params_dict[key] for key in params_dict)

        # Execute the SQL INSERT
        cursor.execute(sql_code, params)
        conn.commit()

        status = "Insert successful"
    except Exception as e:
        status = f"Error inserting data: {e}"
        # print(status)
    finally:
        if "conn" in locals() and conn:
            conn.close()

    return status


def insertNewUser(first, last, email, h_password=None, username=None, ign=None):
    """
    Inserts a new user into the 'users' table.

    This function prepares the data for a new user and calls the generic
    `execute_insert_from_file` utility to perform the insertion. It handles
    both standard and Google-based sign-ups by setting a `g_token` flag. If no
    username is provided, it defaults to the user's email.

    Args:
        first (str): The user's first name.
        last (str): The user's last name.
        email (str): The user's email address.
        h_password (str, optional): The hashed password for the user. Defaults to None.
        username (str, optional): The user's chosen username. Defaults to the email.
        ign (str, optional): The user's Minecraft in-game name. Defaults to None.

    Returns:
        str: A status message from the database insertion operation.
    """
    # print(f"Inserting user with email {email}")

    g_token = None
    # handling gmail token sign up
    if username is None:
        username = email
        g_token = 1
    else:
        g_token = 0

    user_id = str(uuid4())

    insertFile = "insert_newUser.sql"
    insertDict = {
        "user_id": user_id,
        "first": first,
        "last": last,
        "email": email,
        "username": username,
        "h_password": h_password,
        "ign": ign,
        "g_token": g_token,
    }
    status = execute_insert_from_file(insertFolder + insertFile, insertDict)
    # print("Insert user:",status)
    return status



def insertNewIP(email, ipaddress):
    """
    Inserts a new IP address record into the 'iplist' table for a given user.

    This function associates a new IP address with a user, identified by their email.

    Args:
        email (str): The email of the user.
        ipaddress (str): The IP address to be recorded.

    Returns:
        str: A status message from the database insertion operation.
    """
    insertFile = "insert_newIPaddress.sql"
    user_id = getUserIdFromEmail(email)
    if not user_id:
        return "ERROR: There is no user with this email: {email}."
    insertDict = {"user_id": user_id, "ip_address": ipaddress}
    status = execute_insert_from_file(insertFolder + insertFile, insertDict)
    return status


def insertNewConnectionData(email, ipaddress):
    """
    Inserts a new record into the 'connections' table for a given user.

    This function logs initial connection data for a new user, setting the creation,
    last login, and current login IP addresses to the same value. It also calls
    `insertNewIP` to ensure the IP is recorded in the 'iplist' table.

    Args:
        email (str): The email of the user.
        ipaddress (str): The user's current IP address.

    Returns:
        tuple[str, str]: A tuple containing the status of the connection data
                         insertion and the combined status of both insertions.
    """
    insertFile = "insert_newConnection.sql"
    user_id = getUserIdFromEmail(email)
    if not user_id:
        return "ERROR: There is no user with this email: {email}."
    insertDict = {
        "user_id": user_id,
        "createdatip": ipaddress,
        "lastloginip": ipaddress,
        "thisloginip": ipaddress,
    }
    status = execute_insert_from_file(insertFolder + insertFile, insertDict)
    ip_status = insertNewIP(email, ipaddress)
    return status, ip_status



def save_quiz_history(email, results, quiz_config, q_uuid=None, start_ts=None):
    """
    Saves a completed quiz's results to the database for an authenticated user.

    Args:
        email (str): The user's email address.
        results (dict): The dictionary of results from calculate_score.
        quiz_config (dict): The quiz configuration from the session.
        q_uuid (str, optional): An optional UUID to use for the quiz result. If None, a new UUID will be generated.
        start_ts (str, optional): The start timestamp of the quiz. If None, the current timestamp is used.

    Returns:
        str: A status message from the database insertion operation.
    """
    user_id = getUserIdFromEmail(email)
    if not user_id:
        return f"ERROR: There is no user with this email: {email}."

    # Create a dictionary mapping the question's database ID (rowid) to the user's answer.
    # This matches the format used for anonymous quiz results, ensuring consistency.
    answers_by_q_id = {}
    for res in results.get("question_results", []):
        question_db_id = res.get("question", {}).get("db_id")
        if question_db_id:
            answers_by_q_id[str(question_db_id)] = res.get("user_answer", [])
    q_resp_json = json.dumps(answers_by_q_id)

    # Use provided UUID or generate a new one
    if q_uuid is None:
        q_uuid = str(uuid4())

    # Use provided start_ts or generate a new one
    if start_ts is None:
        start_ts = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    insertFile = "insert_newResult.sql"
    insertDict = {
        "q_uuid": q_uuid,
        "q_score": results.get("total_points"),
        "q_year": quiz_config.get("year"),
        "q_percent": quiz_config.get("current_year_percent"),
        "q_resp": q_resp_json,
        "n_correct": results.get("n_correct"),
        "n_wrong": results.get("n_wrong"),
        "n_skip": results.get("n_skip"),
        "user_id": user_id,
        "start_ts": start_ts,
    }

    status = execute_insert_from_file(insertFolder + insertFile, insertDict)
    # print("Save quiz history:", status)
    return status


def insertNewBlacklistEmail(email):
    """
    Inserts a new email into the 'blacklist_emails' table.

    Args:
        email (str): The email to be blacklisted.

    Returns:
        str: A status message from the database insertion operation.
    """
    insertFile = "insert_newBlacklistEmail.sql"
    insertDict = {"email": email}
    status = execute_insert_from_file(insertFolder + insertFile, insertDict)
    return status


def insertNewBlacklistIP(ip_address):
    """
    Inserts a new IP address into the 'blacklist_ips' table.

    Args:
        ip_address (str): The IP address to be blacklisted.

    Returns:
        str: A status message from the database insertion operation.
    """
    insertFile = "insert_newBlacklistIP.sql"
    insertDict = {"ip_address": ip_address}
    status = execute_insert_from_file(insertFolder + insertFile, insertDict)
    return status


def insertNewRegistrationToken(token, ip_address, email):
    """
    Inserts a new registration token into the 'registration_tokens' table.

    Args:
        token (str): The registration token.
        ip_address (str): The user's IP address.
        email (str): The user's email address.

    Returns:
        str: A status message from the database insertion operation.
    """
    insertFile = "insert_newRegistrationToken.sql"
    insertDict = {"token": token, "ip_address": ip_address, "email": email}
    status = execute_insert_from_file(insertFolder + insertFile, insertDict)
    return status
