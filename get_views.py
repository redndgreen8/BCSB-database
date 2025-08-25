import pymssql
import pandas as pd
from getpass import getpass

ppass = getpass("Enter your database password: ")

conn = pymssql.connect(host=, user = , password = ppass, database=)
cursor = conn.cursor()


# Fetch view definitions
cursor.execute("""
SELECT 
    v.name AS view_name, 
    m.definition AS view_definition
FROM 
    sys.views v
JOIN 
    sys.sql_modules m ON v.object_id = m.object_id
""")
views = cursor.fetchall()

# Convert to DataFrame and save as CSV
views_df = pd.DataFrame(views, columns=['view_name', 'view_definition'])
views_df.to_csv('db_views.csv', index=False)

cursor.close()
conn.close()