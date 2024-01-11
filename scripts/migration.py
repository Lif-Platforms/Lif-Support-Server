# ----------------------------
# MySQL Migration Script
# Migrates all data from SQLite to MySQL
#
# Author: Superior126
# Created: 1/11/24
# ----------------------------

# Library imports
import mysql.connector
from mysql.connector.abstracts import ClientFlag
import uuid
import yaml
import sqlite3
import json

# Load main config
with open("config.yml", "r") as config:
    configurations = yaml.safe_load(config.read())
    config.close()

# Connect to SQLite db
sqlite_conn = sqlite3.connect("database/database.db")
sqlite_cursor = sqlite_conn.cursor()

# Connect to MySQL db
mysql_config = {
    "host": configurations['mysql-host'],
    "port": configurations['mysql-port'],
    "user": configurations['mysql-user'],
    "password": configurations['mysql-password'],
    "database": configurations['mysql-database']
}

# Add SSL certificate if SSL is enabled
if configurations['mysql-ssl']:
    # Add SSL configurations
    mysql_config['client_flags'] = [ClientFlag.SSL]
    mysql_config['ssl_ca'] = configurations['mysql-cert-path']

mysql_conn = mysql.connector.connect(**mysql_config)
mysql_cursor = mysql_conn.cursor()

# Select all posts from SQLite database
sqlite_cursor.execute("SELECT * FROM posts")
sqlite_posts = sqlite_cursor.fetchall()

# Sift through SQLite posts
for post in sqlite_posts:
    # Add post to MySQL database
    mysql_cursor.execute("INSERT INTO posts author = %s, title = %s, content = %s, software = %s, post_id = %s, date = %s", 
                         (post[0], post[1], post[2], post[3], post[4], post[6]))

    # Load comments
    sqlite_comments = json.loads(post[5])

    # Sift through SQLite comments and add them to MySQL database
    for comment in sqlite_comments:
        # Generate a unique id for each reply
        reply_id = str(uuid.uuid4())

        # Add reply to database
        mysql_cursor.execute("INSERT INTO replies post_id = %s, reply_id = %s, author = %s, type = %s, content = %s",
                             (post[4], reply_id, comment["Author"], comment["Type"], comment["Content"]))

# Commit all changes to MySQL database
mysql_conn.commit()

# Close MySQL and SQLite connections
mysql_conn.close()
sqlite_conn.close()
