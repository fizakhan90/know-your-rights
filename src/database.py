import snowflake.connector
from config import Config

class Database:
    def __init__(self):
        self.conn = None
        
    def connect(self):
        if not self.conn:
            self.conn = snowflake.connector.connect(Config.SNOWFLAKE_CONFIG)
        return self.conn
    
    def close(self):
        if self.conn:
            self.conn.close()
            self.conn = None
    
    def execute_query(self, query, params=None):
        conn = self.connect()
        try:
            cur = conn.cursor()
            if params:
                cur.execute(query, params)
            else:
                cur.execute(query)
            return cur.fetchall()
        finally:
            self.close()

    def get_rights_by_region(self, region):
        query = """
        SELECT REGION, CATEGORY, RIGHT_TEXT, SOURCES 
        FROM WOMEN_RIGHTS 
        WHERE REGION = %s
        """
        return self.execute_query(query, (region,))

    def get_rights_by_category(self, category):
        query = """
        SELECT REGION, CATEGORY, RIGHT_TEXT, SOURCES 
        FROM WOMEN_RIGHTS 
        WHERE CATEGORY = %s
        """
        return self.execute_query(query, (category,))