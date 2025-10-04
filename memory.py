# memory.py
import sqlite3, threading, os

class Memory:
    def __init__(self, dbfile="pain_memory.db"):
        self.dbfile = dbfile
        self._ensure_dir()
        self.conn = sqlite3.connect(self.dbfile, check_same_thread=False)
        self.lock = threading.Lock()
        self._init_db()

    def _ensure_dir(self):
        d = os.path.dirname(os.path.abspath(self.dbfile))
        if not d:
            return
        os.makedirs(d, exist_ok=True)

    def _init_db(self):
        c = self.conn.cursor()
        c.execute("CREATE TABLE IF NOT EXISTS qa (q TEXT PRIMARY KEY, a TEXT)")
        self.conn.commit()

    def get(self, q):
        c = self.conn.cursor()
        c.execute("SELECT a FROM qa WHERE q = ?", (q,))
        r = c.fetchone()
        return r[0] if r else None

    def save(self, q, a):
        with self.lock:
            c = self.conn.cursor()
            c.execute("INSERT OR REPLACE INTO qa (q,a) VALUES (?,?)", (q,a))
            self.conn.commit()
