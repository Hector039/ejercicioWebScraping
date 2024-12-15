import pymysql.cursors
from dotenv import load_dotenv
import os

load_dotenv()

def dbConn():
    try:
        connection = pymysql.connect(host=os.environ['DB_URL'], 
                                user=os.environ['DB_USER'],
                                password=os.environ['DB_PASS'],
                                database=os.environ['DB_NAME'],
                                charset='utf8mb4',
                                cursorclass=pymysql.cursors.DictCursor)
        return connection
    except Exception as error:
        return f"Message: {error}"
        