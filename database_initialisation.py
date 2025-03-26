import pandas as pd
import numpy as np
import pymysql
from sqlalchemy import create_engine
import getpass  # To get the password without showing the input
password = getpass.getpass()

import mysql.connector

# Connect to MySQL (you can also specify host, user, password)
conn = mysql.connector.connect(
    host='your_host',
    user='your_user',
    password='your_password'
)

cursor = conn.cursor()

# Create a new database
cursor.execute("CREATE DATABASE IF NOT EXISTS my_database")

# Use the newly created database
cursor.execute("USE my_database")

# Create a table
cursor.execute("""
    CREATE TABLE IF NOT EXISTS example_table (
        id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(255) NOT NULL,
        date_created TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
""")

# Commit changes and close the connection
conn.commit()
cursor.close()
conn.close()
