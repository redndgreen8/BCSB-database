import pymssql
from getpass import getpass


#The host.ip.address is the ip of the host server. The dba group in your organization should know this. 
#The username has to be preceded with the 'DEFAULT_REALM\\' from Microsoft SQL Server for Mac users. You should be able to get this from the dba group in your organization as well. 
#The username and password will be the same as your Windows/Okta username and password. 
#The database is just the database name you want to connect to. 

ppass = getpass("Enter your database password: ")

conn = pymssql.connect(host=, user = , password = ppass, database=)
cursor = conn.cursor()

cursor.execute("SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_TYPE = 'BASE TABLE'")
tables = cursor.fetchall()

# Open a file to write Cypher commands
with open('import_to_neo4j.cql', 'w') as file:
    # Create nodes for tables
    for table in tables:
        file.write(f"CREATE (:Table {{name: '{table[0]}'}});\n")

    # Create nodes for columns and relationships from tables to columns
    for table in tables:
        cursor.execute(f"SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = '{table[0]}'")
        columns = cursor.fetchall()
        for column in columns:
            file.write(f"CREATE (:Column {{name: '{column[0]}'}});\n")
            file.write(f"MATCH (t:Table {{name: '{table[0]}'}}), (c:Column {{name: '{column[0]}'}}) CREATE (t)-[:HAS_COLUMN]->(c);\n")

    # Foreign key relationships
    cursor.execute("""
    SELECT 
        fk.name AS FK_name, 
        tp.name AS parent_table, 
        tr.name AS ref_table, 
        cp.name AS parent_column, 
        cr.name AS ref_column 
    FROM 
        sys.foreign_keys AS fk
    INNER JOIN 
        sys.tables AS tp ON fk.parent_object_id = tp.object_id
    INNER JOIN 
        sys.tables AS tr ON fk.referenced_object_id = tr.object_id
    INNER JOIN 
        sys.foreign_key_columns AS fkc ON fkc.constraint_object_id = fk.object_id
    INNER JOIN 
        sys.columns AS cp ON fkc.parent_column_id = cp.column_id AND fkc.parent_object_id = cp.object_id
    INNER JOIN 
        sys.columns AS cr ON fkc.referenced_column_id = cr.column_id AND fkc.referenced_object_id = cr.object_id
    """)
    relations = cursor.fetchall()
    for relation in relations:
        file.write(f"MATCH (t1:Table {{name: '{relation[1]}'}}), (t2:Table {{name: '{relation[2]}'}}) CREATE (t1)-[:FOREIGN_KEY_TO {{name: '{relation[0]}', parent_column: '{relation[3]}', ref_column: '{relation[4]}'}}]->(t2);\n")

cursor.close()
conn.close()