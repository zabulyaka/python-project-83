from psycopg2.extras import DictCursor


class UrlsRepository:
    def __init__(self, conn):
        self.conn = conn

    def add_url(self, data):
        with self.conn.cursor() as cur:
            cur.execute("""
                INSERT INTO urls (name, created_at)
                VALUES (%s, %s)
                RETURNING id
            """, data)
            url_id = cur.fetchone()[0]
        self.conn.commit()
        return url_id

    def get_urls(self):
        with self.conn.cursor(cursor_factory=DictCursor) as cur:
            cur.execute("""
                SELECT * FROM urls;
            """)
            return [dict(row) for row in cur]

    def find_url(self, id):
        with self.conn.cursor(cursor_factory=DictCursor) as cur:
            cur.execute("""
                SELECT * FROM urls WHERE id = %s;
            """, (id,))
            row = cur.fetchone()
            return dict(row) if row else None
