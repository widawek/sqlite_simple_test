import sqlite3
from sqlite3 import Error


class SqlPractice:
    def __init__(self, db_file, test_only=False):
        if not test_only:
            self.conn = self.create_connection(db_file)
        else:
            self.conn = self.create_connection_in_memory()

    def create_connection(self, db_file):
        """ create a database connection to a SQLite database """
        try:
            conn = sqlite3.connect(db_file)
            print(f"Connected to {db_file}, sqlite version: {sqlite3.version}")
            return conn
        except Error as e:
            print(e)

    def create_connection_in_memory(self):
        """ create a database connection to a SQLite database """
        try:
            conn = sqlite3.connect(":memory:")
            print(f"Connected, sqlite version: {sqlite3.version}")
            return conn
        except Error as e:
            print(e)

    def execute_sql(self, sql):
        """ Execute sql """
        try:
            c = self.conn.cursor()
            c.execute(sql)
            self.conn.commit()
        except Error as e:
            print(e)

    def add_data(self, table, data):
        """ Create a new row into the table """
        cur = self.conn.cursor()
        cur.execute(f"SELECT * FROM {table}")
        column_names = tuple([description[0] for description in cur.description])
        vals = '?,' * len(column_names)
        sql = f'''INSERT INTO {table}{column_names} VALUES({vals[:-1]})'''
        cur.execute(sql, data)
        self.conn.commit()
        return cur.lastrowid

    def update(self, table, strategy, **kwargs):
        """
        Update a row in a table
        :param table: table name
        :param strategy: strategy value of the row to be updated
        :param kwargs: key-value pairs to update
        :return:
        """
        parameters = [f"{k} = ?" for k in kwargs]
        parameters_str = ", ".join(parameters)
        values = tuple(v for v in kwargs.values())
        values += (strategy, )

        sql = f"""UPDATE {table}
                  SET {parameters_str}
                  WHERE strategy = ?"""

        with self.conn:
            try:
                cur = self.conn.cursor()
                cur.execute(sql, values)
                self.conn.commit()
                print("Update successful")
            except sqlite3.OperationalError as e:
                print(f"An error occurred: {e}")

    def delete_all(self, table):
        """ Delete all rows from table """
        sql = f'DELETE FROM {table}'
        with self.conn:
            cur = self.conn.cursor()
            cur.execute(sql)
        print("Deleted")
