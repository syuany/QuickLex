import sqlite3
from pathlib import Path
from typing import Optional, Dict
import os, sys


def get_date_path():
    dev_path = os.path.join(os.path.dirname(__file__), "../../data/ecdict.db")
    if getattr(sys, "frozen", False):
        base_path = os.path.dirname(sys.executable)
        return os.path.join(base_path, "data/ecdict.db")
    elif os.path.exists(dev_path):
        return dev_path
    else:
        raise FileNotFoundError("DB NOT FOUND")


class DictionaryDB:
    def __init__(self):
        # 初始化DictionaryDB，设置数据库路径
        db_path = get_date_path()
        self.db_path = Path(db_path)
        # self._create_table()

    def _create_table(self):
        # 创建数据库表和索引（如果不存在）
        self.db_path.parent.mkdir(exist_ok=True)
        with self.connect() as conn:
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS words(
                    id INTEGER PRIMARY KEY,
                    word VARCHAR(64) NOT NULL,
                    sw VARCHAR(64) NOT NULL
                    phonetic TEXT,
                    defination TEXT,
                    translation TEXT,
                )
            """
            )
        conn.execute("CREATE INDEX IF NOT EXISTS idx_word ON stardict(words)")

    def connect(self):
        # 建立数据库连接
        return sqlite3.connect(self.db_path)

    def query_word(self, word: str) -> Optional[Dict]:
        # 根据单词查询数据库中的信息
        with self.connect() as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.execute(
                "SELECT * FROM stardict WHERE word = ?", (word.lower(),)
            )
            result = cursor.fetchone()
            return dict(result) if result else None

    def fuzzy_query(self, keyword: str, limit=10) -> list:
        with self.connect() as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.execute(
                "SELECT * FROM stardict WHERE word LIKE ? ORDER BY length(word) LIMIT ?",
                (f"%{keyword}%", limit),
            )
            return [dict(row) for row in cursor.fetchall()]

    def import_from_csv(self, csv_path: str):
        # 从CSV文件导入数据到数据库
        pass  # TODO
