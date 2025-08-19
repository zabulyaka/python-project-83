import psycopg2
from psycopg2.extras import DictCursor


class DatabaseConnection:
    def __init__(self, db_url):
        self.db_url = db_url

    def __enter__(self):
        self.conn = psycopg2.connect(
            self.db_url,
            cursor_factory=DictCursor
        )
        with self.conn as conn:
            return conn.cursor()

    def __exit__(self, type, value, traceback):
        self.conn.commit()
        self.conn.close()

class UrlsRepository:
    def __init__(self, db_url):
        self.cursor = DatabaseConnection(db_url)

    
#    def __init__(self, conn):
#        self.conn = conn
    
#    def create_table(self):
#        with self.conn.cursor() as cur:
#            cur.execute("""
#                DROP TABLE IF EXISTS urls;
#
#                CREATE TABLE urls (
#                    id BIGINT PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
#                    name VARCHAR(255) UNIQUE NOT NULL,
#                    created_at DATE DEFAULT CURRENT_TIMESTAMP
#                );
#            """)
#        self.conn.commit()

    def add_url(self, data):
#        with self.conn.cursor() as cur:
#            cur.execute("""
#                INSERT INTO urls (name)
#                VALUES (%s)
#                RETURNING id
#            """, data)
#            url_id = cur.fetchone()[0]
#        self.conn.commit()
        query = '''
            INSERT INTO urls(name)
            VALUES (%s)
            RETURNING id
        '''
        with self.cursor as cur:
            cur.execute(query, data)
            url_id = cur.fetchone()[0]
            return url_id

    def get_urls(self):
        query = '''
            SELECT * FROM urls;
        '''
        with self.cursor as cur:
            cur.execute(query)
            return [dict(row) for row in cur]
#        with self.conn.cursor(cursor_factory=DictCursor) as cur:
#            cur.execute("""
#                SELECT * FROM urls;
#            """)
#            return [dict(row) for row in cur]

    def find_url(self, id):
        query = '''
            SELECT * FROM urls WHERE id = %s;
        '''
        with self.cursor as cur:
            cur.execute(query, (id,))
            row = cur.fetchone()
#        with self.conn.cursor(cursor_factory=DictCursor) as cur:
#            cur.execute("""
#                SELECT * FROM urls WHERE id = %s;
#            """, (id,))
#            row = cur.fetchone()
            return dict(row) if row else None
