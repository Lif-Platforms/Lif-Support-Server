# ----------------------------------
# Title: Config Template
# Description: Holds the default configuration values for the "config.yml".
# Author: Superior126
# Date: 11/22/23
# ----------------------------------

default_config = {
    "allow-origins": ['http://localhost:3000'],
    "auth-url":  "http://localhost:8002",
    "auth-access-token": "INSERT_TOKEN_HERE",
    "mail-service-token": "INSERT_TOKEN_HERE",
    "mail-service-url": "http://localhost:8005",
    "mysql-host": "localhost",
    "mysql-port": 3306,
    "mysql-user": "root",
    "mysql-password": "INSERT_PASSWORD_HERE",
    "mysql-database": "INSERT_DATABASE_HERE",
    "mysql-ssl": False,
    "mysql-cert-path": "INSERT_CERT_PATH_HERE"
}