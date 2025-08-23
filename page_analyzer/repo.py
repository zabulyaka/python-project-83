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

    def add_url(self, data):
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
            SELECT DISTINCT ON (urls.id)
                urls.id,
                urls.name,
                url_checks.status_code,
                url_checks.created_at
            FROM urls
            LEFT JOIN url_checks ON
                urls.id = url_checks.url_id
            ORDER BY id, created_at DESC;
        '''
        with self.cursor as cur:
            cur.execute(query)
            return [dict(row) for row in cur]

    def find_url(self, id):
        query = '''
            SELECT * FROM urls WHERE id = %s;
        '''
        with self.cursor as cur:
            cur.execute(query, (id,))
            row = cur.fetchone()
            return dict(row) if row else None

    def add_url_check(self, data):
        query = '''
            INSERT INTO url_checks (
                url_id,
                status_code,
                h1,
                title,
                description
            )
            VALUES (%s, %s, %s, %s, %s)
        '''
        with self.cursor as cur:
            cur.execute(query, data)

    def get_url_checks(self, id):
        query = '''
            SELECT * FROM url_checks
            WHERE url_id = (%s)
        '''
        with self.cursor as cur:
            cur.execute(query, (id,))
            checks = cur.fetchall()
            return checks
