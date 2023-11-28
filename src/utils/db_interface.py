import sqlite3
import json
from datetime import datetime

def new_post(author, title, content, software, post_id):
    # Connects to database
    conn = sqlite3.connect("database/database.db")
    c = conn.cursor()

    # Get Current Date
    current_date = datetime.today().strftime('%m/%d/%Y')

    # Adds post to database
    c.execute("INSERT INTO posts (author, title, content, software, id, comments, date) VALUES (?, ?, ?, ?, ?, ?, ?)", (author, title, content, software, post_id, "[]", current_date))
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

def get_post(post_id: str):
    # Connects to database
    conn = sqlite3.connect("database/database.db")
    c = conn.cursor()

    # Get post from database
    c.execute("SELECT * FROM posts WHERE id = ?", (post_id,))
    post = c.fetchone()

    return post

def create_comment(author, comment, post_id):
    # Connects to database
    conn = sqlite3.connect("database/database.db")
    c = conn.cursor()

    # Execute a SELECT query to retrieve posts
    c.execute("SELECT * FROM posts")
    posts = c.fetchall()

    # Gets post
    for post in posts:
        database_post_id = post[4]

        if post_id == database_post_id:
            comments = json.loads(post[5])

            # Adds to comments
            comments.append({"Author": author, "Content": comment, "Type": "Comment"})

            # Updates database
            conn.execute(f"""UPDATE posts SET comments = '{json.dumps(comments)}'
                                        WHERE Id = '{post_id}'""")
            
    conn.commit()
    conn.close()

def create_answer(author, answer, post_id):
    # Connects to database
    conn = sqlite3.connect("database/database.db")
    c = conn.cursor()

    # Execute a SELECT query to retrieve posts
    c.execute("SELECT * FROM posts")
    posts = c.fetchall()

    # Gets post
    for post in posts:
        database_post_id = post[4]

        if post_id == database_post_id:
            answers = json.loads(post[5])

            # Adds to comments
            answers.append({"Author": author, "Content": answer, "Type": "Answer"})

            # Updates database
            conn.execute(f"""UPDATE posts SET comments = '{json.dumps(answers)}'
                                        WHERE Id = '{post_id}'""")
            
    conn.commit()
    conn.close()

def get_recent_posts():
    # Connects to database
    conn = sqlite3.connect("database/database.db")
    c = conn.cursor()

    # Execute a SELECT query to retrieve posts
    c.execute("SELECT * FROM posts ORDER BY id DESC LIMIT 5")
    posts = c.fetchall()

    # This is what the function will return after the data is formatted
    return_posts = []

    for post in posts:
        raw_content = post[2]

        # Adds "..." if the content is too long for the preview
        if len(raw_content) <= 100:
            content = raw_content
        else:
            content =  raw_content[:100 - 3] + "..."

        return_posts.append({"Title": post[1], "Content": content, "Software": post[3], "Id": post[4]})

    return return_posts

def get_post_author(post_id: str):
    # Connects to database
    conn = sqlite3.connect("database/database.db")
    c = conn.cursor()

    c.execute ("SELECT * FROM posts WHERE id = ?", (post_id,))
    row = c.fetchone ()

    # Fetch username from row 
    username = row[0]

    return username