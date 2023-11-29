import mysql.connector
import json
from datetime import datetime
import uuid

# Allow main script to set the config
def set_config(config):
    global configurations
    configurations = config

# Handle database connection
def connect_to_database():
    # Handle connecting to the database
    def connect():
        global conn
        conn = mysql.connector.connect(
            host=configurations['mysql-host'],
            user=configurations['mysql-user'],
            password=configurations['mysql-password'],
            database=configurations['mysql-database']
        )
    
    # Check if there is a MySQL connection
    if conn is None:
        connect()
    else:
        # Check if existing connection is still alive
        if not conn.is_connected():
            connect()


def new_post(author, title, content, software, post_id):
    connect_to_database()

    cursor = conn.cursor()

    # Get Current Date
    current_date = datetime.today().strftime('%m/%d/%Y')

    # Adds post to database
    cursor.execute("INSERT INTO posts (author, title, content, software, post_id, date) VALUES (?, ?, ?, ?, ?, ?)", (author, title, content, software, post_id, current_date))
    conn.commit()

    cursor.close()

def get_posts():
    connect_to_database()

    cursor = conn.cursor()

    # Execute a SELECT query to retrieve posts
    cursor.execute("SELECT * FROM posts")
    posts = cursor.fetchall()

    cursor.close()

    return posts

def get_post(post_id: str):
    connect_to_database()
    
    cursor = conn.cursor()

    # Get post from database
    cursor.execute("SELECT * FROM posts WHERE id = ?", (post_id,))
    post = cursor.fetchone()

    return post

def create_comment(author, comment, post_id):
    connect_to_database()

    cursor = conn.cursor()

    # Check if post exists
    cursor.execute("SELECT * FROM posts WHERE post_id = ?", (post_id,))
    post = cursor.fetchone()

    if post: 
        # Generate unique id for reply 
        reply_id = str(uuid.uuid4())

        # Create new post reply
        cursor.execute("INSERT INTO replies (post_id, reply_id, author, type, content)", (post_id, reply_id, author, "Comment", comment))
        conn.commit()
        cursor.close()

        return True
    else:
        cursor.close()
        return False

def create_answer(author, answer, post_id):
    connect_to_database()

    cursor = conn.cursor()

    # Check if post exists
    cursor.execute("SELECT * FROM posts WHERE post_id = ?", (post_id,))
    post = cursor.fetchone()

    if post: 
        # Generate unique id for reply 
        reply_id = str(uuid.uuid4())

        # Create new post reply
        cursor.execute("INSERT INTO replies (post_id, reply_id, author, type, content)", (post_id, reply_id, author, "Answer", answer))
        conn.commit()
        cursor.close()

        return True
    else:
        cursor.close()
        return False

def get_recent_posts():
    connect_to_database()

    cursor = conn.cursor()

    # Execute a SELECT query to retrieve posts
    cursor.execute("SELECT * FROM posts ORDER BY id DESC LIMIT 5")
    posts = cursor.fetchall()

    # This is what the function will return after the data is formatted
    return_posts = []

    for post in posts:
        raw_content = post[3]

        # Adds "..." if the content is too long for the preview
        if len(raw_content) <= 100:
            content = raw_content
        else:
            content =  raw_content[:100 - 3] + "..."

        return_posts.append({"Title": post[2], "Content": content, "Software": post[4], "Id": post[5]})

    return return_posts

def get_post_author(post_id: str):
    connect_to_database()

    cursor = conn.cursor()

    cursor.execute ("SELECT * FROM posts WHERE id = ?", (post_id,))
    row = cursor.fetchone()
    cursor.close()

    # Return username from row 
    if row:
        return row[1]
    else:
        return None

def delete_post(post_id: str):
    connect_to_database()

    cursor = conn.cursor()

    # Delete post from database
    cursor.execute("DELETE FROM posts WHERE post_id = ?", (post_id,))

    # Delete all replies from database
    cursor.execute("DELETE FROM replies WHERE post_id = ?", (post_id,))

    # Commit and close database cursor
    conn.commit()
    cursor.close()

def update_post(post_id: str, title: str, content: str, software: str):
    connect_to_database()

    cursor = conn.cursor()

    # Update post in database
    cursor.execute('UPDATE posts SET title = ?, content = ?, software = ? WHERE post_id = ?', (title, content, software, post_id))

    # Commit and close database cursor
    conn.commit()
    cursor.close()