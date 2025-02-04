
import mysql.connector
import json

def execute_query_in_db(host: str, port: int, user: str, password: str, database: str, query: str):
    try:
        # connect to db and get cursor
        db_connection = mysql.connector.connect(
            host=host,
            port=port,
            user=user,
            password=password,
            database=database
        )
        db_cursor = db_connection.cursor()

        # get the query and return the json
        db_cursor.execute(query)
        result_set = db_cursor.fetchall()
        column_names = [desc[0] for desc in db_cursor.description]
        results = [dict(zip(column_names, row)) for row in result_set]
        json_result = json.dumps(results, indent=4)

        # return json
        return json_result
        
    except:
        return ""
    finally:
        db_cursor.close()
        db_connection.close()

def get_schema_in_db(host: str, port: int, user: str, password: str, database: str):
    try:
        # connect to db and get cursor
        db_connection = mysql.connector.connect(
            host=host,
            port=port,
            user=user,
            password=password,
            database=database
        )
        db_cursor = db_connection.cursor()

        # get the query and return the json
        db_cursor.execute(f"SELECT * FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_SCHEMA = '{database}';")
        result_set = db_cursor.fetchall()
        column_names = [desc[0] for desc in db_cursor.description]
        results = [dict(zip(column_names, row)) for row in result_set]

        # return json
        return results
        
    except:
        return {}

