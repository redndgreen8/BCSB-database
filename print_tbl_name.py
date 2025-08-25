import pymssql
from getpass import getpass


#The host.ip.address is the ip of the host server. The dba group in your organization should know this. 
#The username has to be preceded with the 'DEFAULT_REALM\\' from Microsoft SQL Server for Mac users. You should be able to get this from the dba group in your organization as well. 
#The username and password will be the same as your Windows/Okta username and password. 
#The database is just the database name you want to connect to. 

ppass = getpass("Enter your database password: ")

conn = pymssql.connect(host=, user = , password = ppass, database=)
cursor = conn.cursor()

cursor.execute('SELECT table_name FROM information_schema.tables')
tables = cursor.fetchall()
for table in tables:
    print(table[0])