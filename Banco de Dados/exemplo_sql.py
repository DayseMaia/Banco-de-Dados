import psycopg2

conn = psycopg2.connect(dbname = "Escola", host = "localhost", port = "5432", user = "postgres", password = "postgres")
cursor = conn.cursor()

cursor.execute('''
SELECT * FROM "alunos"
''')

print(cursor.fetchall())

for aluno in cursor.fetchall():
    print(f"{aluno[0]} - {aluno[2]}")

