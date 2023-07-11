import sqlite3
import uuid

def new_post(author, title, content, software):
    # Generate a random UUID
    post_id = str(uuid.uuid4())

    # Connects to database
    conn = sqlite3.connect("database/database.db")
    c = conn.cursor()

    # Adds post to database
    c.execute("INSERT INTO posts (author, title, content, software, id) VALUES (?, ?, ?, ?, ?)", (author, title, content, software, post_id))
    conn.commit()

    conn.close()


def get_posts():
    # Connects to database
    conn = sqlite3.connect("database/database.db")
    c = conn.cursor()

    # Execute a SELECT query to retrieve posts
    c.execute("SELECT * FROM posts")
    posts = c.fetchall()

    conn.close()

    return posts