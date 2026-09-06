import sqlite3
from datetime import datetime

MEMORY_DB = "agent_memory.db"

def initialize_memory():
    conn = sqlite3.connect(MEMORY_DB)
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS memories (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        question TEXT,
        investigation TEXT,
        decision TEXT,
        created_at TEXT
    )
    """)

    conn.commit()
    conn.close()

def save_memory(question, investigation, decision):
    conn = sqlite3.connect(MEMORY_DB)
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO memories
    (question, investigation, decision, created_at)
    VALUES (?, ?, ?, ?)
    """, (
        question,
        investigation,
        decision,
        datetime.now().isoformat()
    ))

    conn.commit()
    conn.close()

def search_memory(query):
    conn = sqlite3.connect(MEMORY_DB)
    cursor = conn.cursor()

    words = query.lower().split()

    cursor.execute("""
    SELECT question, investigation, decision, created_at
    FROM memories
    ORDER BY id DESC
    LIMIT 20
    """)

    rows = cursor.fetchall()
    conn.close()

    results = []

    for row in rows:
        text = " ".join(str(x).lower() for x in row)

        if any(word in text for word in words if len(word) > 3):
            results.append({
                "question": row[0],
                "investigation": row[1],
                "decision": row[2],
                "created_at": row[3]
            })

    return results[:5]