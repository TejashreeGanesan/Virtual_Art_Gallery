import mysql.connector
from util.DBPropertyUtil import PropertyUtil

class DBConnection:
    _connection = None

    @staticmethod
    def get_connection():
        if DBConnection._connection is None:
            props = PropertyUtil.get_property_string()
            if props:
                try:
                    DBConnection._connection = mysql.connector.connect(
                        host = props.get('host'),
                        port = props.get('port'),
                        database = props.get('database'),
                        user = props.get('user'),
                        password = props.get('password')
                    )
                except mysql.connector.Error as e:
                    print(f"Error connecting to MySql: {e}")
            else:
                print(f"Properties could not be loaded")
        return DBConnection._connection