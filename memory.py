# memory.py
import sqlite3
import time

class QAStorage:
    def __init__(self, path="pain_memory.db"):
        self.path = path
        self._ensure()

    def _ensure(self):
        conn = sqlite3.connect(self.path)
        c = conn.cursor()
        c.execute('''
            CREATE TABLE IF NOT EXISTS qa (
                id INTEGER PRIMARY KEY,
                question TEXT UNIQUE,
                answer TEXT,
                source TEXT,
                timestamp INTEGER
            )
        ''')
        conn.commit()
        conn.close()

    def save_qa(self, question, answer, source="local"):
        now = int(time.time())
        conn = sqlite3.connect(self.path)
        c = conn.cursor()
        try:
            c.execute("INSERT OR REPLACE INTO qa (question, answer, source, timestamp) VALUES (?, ?, ?, ?)",
                      (question, answer, source, now))
        except Exception:
            pass
        conn.commit()
        conn.close()

    def find_answer(self, question):
        conn = sqlite3.connect(self.path)
        c = conn.cursor()
        c.execute("SELECT answer FROM qa WHERE question = ?", (question,))
        r = c.fetchone()
        conn.close()
        return r[0] if r else None

    def list_all(self):
        conn = sqlite3.connect(self.path)
        c = conn.cursor()
        c.execute("SELECT question, answer, source, timestamp FROM qa ORDER BY timestamp DESC")
        r = c.fetchall()
        conn.close()
        return r
