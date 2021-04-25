import csv
import psycopg2
postgressql_url = "postgres://rlqrzgzdhjvlyd:a4cf6f365b690986f881b5ff776bd97ecb6236099a256bcc58024856974e6f69@ec2-34-194-215-27.compute-1.amazonaws.com:5432/da19esl0rg7tu0"
connection = psycopg2.connect(postgressql_url)

try:
    with connection:
        with connection.cursor() as cursor:
            cursor.execute("CREATE TABLE books (isbn VARCHAR(100) NOT NULL PRIMARY KEY, title VARCHAR(200) NOT NULL,author VARCHAR(100) NOT NULL,year VARCHAR(100));")
except:
    pass

cursor = connection.cursor()
with open('books.csv','r') as file:
     reader = csv.reader(file)
     next(reader)
     for row in reader:
        cursor.execute(
        "INSERT INTO books VALUES (%s, %s, %s, %s)",
        row
    )
connection.commit()