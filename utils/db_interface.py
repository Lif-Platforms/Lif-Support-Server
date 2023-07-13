import sqlite3
import uuid
import json

def new_post(author, title, content, software):
    # Generate a random UUID
    post_id = str(uuid.uuid4())

    # Connects to database
    conn = sqlite3.connect("database/database.db")
    c = conn.cursor()

    # Adds post to database
    c.execute("INSERT INTO posts (author, title, content, software, id, comments) VALUES (?, ?, ?, ?, ?, ?)", (author, title, content, software, post_id, "[]"))
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