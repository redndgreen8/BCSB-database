dispositionflag
datetimephoneconsult
activities_preference
dtcompletesurvey
clinic
consentsignedtracker
baselinesurveystatus
baselineblooddrawstatus
crflatest_externalrequest
crflatest_externalentry


import pymssql
from getpass import getpass
import csv
from datetime import datetime


#The host.ip.address is the ip of the host server. The dba group in your organization should know this. 
#The username has to be preceded with the 'DEFAULT_REALM\\' from Microsoft SQL Server for Mac users. You should be able to get this from the dba group in your organization as well. 
#The username and password will be the same as your Windows/Okta username and password. 
#The database is just the database name you want to connect to. 

ppass = getpass("Enter your database password: ")

conn = pymssql.connect(host=, user = , password = ppass, database=)
cursor = conn.cursor()


query = """
SELECT bcsbusername, dispositionflag, datetimephoneconsult, activities_preference, dtcompletesurvey, clinic, consentsignedtracker, baselinesurveystatus, baselineblooddrawstatus, crflatest_externalrequest, crflatest_externalentry, dateconsentsignedbypt, dateconsentsignedbypt_v2, dateconsentsignedbypt_v2_v3, dateconsentsignedbypt_v2sp
FROM RedCapData
WHERE NOT (
    dispositionflag IS NULL AND
    datetimephoneconsult IS NULL AND
    activities_preference IS NULL AND
    dtcompletesurvey IS NULL AND
    clinic IS NULL AND
    consentsignedtracker IS NULL AND
    baselinesurveystatus IS NULL AND
    baselineblooddrawstatus IS NULL AND
    crflatest_externalrequest IS NULL AND
    crflatest_externalentry IS NULL
    dateconsentsignedbypt_v2sp IS NULL AND
    dateconsentsignedbypt IS NULL AND
    dateconsentsignedbypt_v2 IS NULL AND
    dateconsentsignedbypt_v2_v3 IS NULL 

);
"""


current_date = datetime.now().strftime("%Y%m%d")

output_path = f'RedCapOut_enrollment_{current_date}.csv'


cursor.execute(query)

with open(output_path, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow([i[0] for i in cursor.description])

    # Write the data rows
    for row in cursor:
        writer.writerow(row)

cursor.close()
conn.close()