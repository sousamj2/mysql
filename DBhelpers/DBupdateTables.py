# import sqlite3
from datetime import datetime
from .DBselectTables import getUserIdFromEmail
from .DBbaseline import get_mysql_connection
import os
updateFolder = os.path.join(os.path.dirname(__file__), "..", "MySQLqueries", "updateHandler", "")

def refresh_last_login_and_ip(email, current_ip):
    conn = get_mysql_connection()
    if not conn:
        raise ConnectionError("Could not connect to MySQL database")

    try:
        # Read SQL code from file
        with open(updateFolder + "update_last_login_and_ip.sql", 'r') as file:
            sql_code = file.read()
            sql_code = sql_code.replace("?","%s")

        cursor = conn.cursor()
        now = datetime.now()

        user_id = getUserIdFromEmail(email)

        cursor.execute(sql_code, (now, current_ip, user_id,))
        conn.commit()

        status = "Time stamps and IP updated."
    except Exception as e:
        status = f"Error updating data: {e}"
    finally:
        conn.close()

    return status

def update_mc_stats(email, uuid, rank, bank, claims, last_online):
    conn = get_mysql_connection()
    if not conn:
        return "Error: DB connection failed"
    try:
        # Convert "NA" to None for database compatibility
        uuid = None if uuid == "NA" else uuid
        rank = None if rank == "NA" else rank
        bank = None if bank == "NA" else bank
        claims = None if claims == "NA" else claims
        
        with open(updateFolder + "update_mc_stats.sql", 'r') as file:
            sql_code = file.read()
        cursor = conn.cursor()
        cursor.execute(sql_code, (uuid, rank, bank, claims, last_online, email))
        conn.commit()
        print(f"[DEBUG] DB Sync Success: {cursor.rowcount} row(s) updated for {email}", flush=True)
        return "MC stats updated"
    except Exception as e:
        print(f"[DEBUG] DB Sync ERROR: {e}", flush=True)
        return f"Error: {e}"
    finally:
        conn.close()