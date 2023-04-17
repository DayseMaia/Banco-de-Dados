import psycopg2


try:
    conn = psycopg2.connect(dbname = "Escola2", host = "localhost", port = "5432", user = "postgres", password = "postgres")
    
    cursor = conn.cursor()

    print("Conectado com sucesso!")

    # cursor.execute('''
    # CREATE TABLE "Alunos" (
    # "NroMatricula" SERIAL PRIMARY KEY,
    # "Nome" VARCHAR (255) NOT NULL,
    # "CPF" CHAR(11) NOT NULL,
    # "Endereço" VARCHAR(255) DEFAULT 'Não Informado!',
    # "Telefone" CHAR(11) DEFAULT 'XX-XXXX',
    # "Ano Nascimento" INT
    # )
    # ''')


    cursor.execute('''
    INSERT INTO "Alunos"
    VALUES(DEFAULT, 'João', '12345678912', DEFAULT, DEFAULT, 2023)
    ''')
    
    conn.commit()

    conn.close()

except(Exception, psycopg2.Error) as error:
    print("Ocorreu um erro!", error)