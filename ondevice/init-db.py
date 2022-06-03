import mysql.connector as mysql
import os
from dotenv import load_dotenv #only required if using dotenv for creds
 
load_dotenv('credentials.env')

db_host = os.environ['MYSQL_HOST']
db_user = os.environ['MYSQL_USER']
db_pass = os.environ['MYSQL_PASSWORD']
db_name = os.environ['MYSQL_DATABASE']

db = mysql.connect(user=db_user, password=db_pass, host=db_host, database=db_name)
cursor = db.cursor()
cursor.execute("DROP TABLE IF EXISTS Speech2Text;")
 
try:
  cursor.execute("""
    CREATE TABLE Speech2Text (
      id          integer AUTO_INCREMENT PRIMARY KEY,
      text        VARCHAR(255),
      time        TIMESTAMP
    );
  """)

except RuntimeError as err:
  print("runtime error: {0}".format(err))