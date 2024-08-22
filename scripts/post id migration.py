import mysql.connector
from mysql.connector.abstracts import ClientFlag
import yaml

print("Starting migration process...")

# Load main config
with open("config.yml", "r") as config:
    configurations = yaml.safe_load(config.read())
    config.close()

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

# Get all replies
mysql_cursor.execute("SELECT * FROM replies")
replies = mysql_cursor.fetchall()

# Parse through all replies
for reply in replies:
    mysql_cursor.execute("SELECT id FROM posts WHERE post_id = %s", (reply[1],))
    post = mysql_cursor.fetchone()

    if post:
        mysql_cursor.execute("UPDATE replies SET post_id = %s WHERE reply_id = %s", (post[0], reply[2]))

# Commit all changes
mysql_conn.commit()
mysql_conn.close()

print("Migration Complete!")