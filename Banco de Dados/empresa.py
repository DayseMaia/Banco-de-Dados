#Entidade Funcionários:

# Id_Func: INT AUTO GENERATED (PK),
# Nome: CHAR(255) NOT NULL,
# Salario: FLOAT(2) NOT NULL DEFAULT 0.00
# Cargo: CHAR(255) NOT NULL DEFAULT 'Autônomo',
# Id_Departamento: INT (FK)

#Entidade Departamentos:

# Id_Departamento: INT AUTO GENERATED (PK),
# Nome_Departamento: CHAR(255)
# Id_Gerente: INT (FK)

import psycopg2

# def criar_tabela_funcionario():
#     sql = '''
#     CREATE TABLE "Funcionario" (
#     "Id_Func" INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
#     "Nome" VARCHAR(255) NOT NULL,
#     "Salario" MONEY NOT NULL DEFAULT 0,
#     "Cargo" VARCHAR(255) NOT NULL DEFAULT 'Autônomo',
#     "Id_Dept" INT NOT NULL DEFAULT 1
#     )
#     '''
#     return sql

# def criar_tabela_departamento():
#     sql = '''
#     CREATE TABLE "Departamento" (
#     "Id" INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
#     "Nome" VARCHAR(255) NOT NULL
#     )
#     '''
#     return sql

# try:
#     conn = psycopg2.connect(dbname = "XYZ Soluções", host = "localhost", port = "5432", user = "postgres", password = "postgres")
#     cursor = conn.cursor() 

#     # cursor.execute(criar_tabela_funcionario())
#     # conn.commit()

#     # cursor.execute(criar_tabela_departamento())
#     # conn.commit()

#     print("Tabelas criadas!")

#     cursor.close()
#     conn.close()

# except(Exception, psycopg2.Error) as error:
#     print("Ocorreu um erro!", error)


###############################################

try:
    conn = psycopg2.connect(dbname = "XYZ Soluções", host = "localhost", port = "5432", user = "postgres", password = "postgres")
    cursor = conn.cursor() 

except(Exception, psycopg2.Error) as error:
    print("Ocorreu um erro!", error)

def ver_funcionario():
    cursor.execute('''
    SELECT * FROM "Funcionario"
    ORDER BY "Id_Func" ASC
    ''')
    lista_funcionarios = cursor.fetchall()
    print(lista_funcionarios)

def ver_departamento():
    cursor.execute('''
    SELECT * FROM "Departamento"
    ORDER BY "Id" ASC
    ''')
    lista_departamentos = cursor.fetchall()
    print(lista_departamentos)

def inserir_funcionario():
    print("Você está cadastrando um novo funcionário. ")

    nome_novo_funcionario = input("Digite o nome do funcionário: ")
    salario_novo_funcionario = input("Digite o salário do novo funcionário: ")
    cargo_novo_funcionario = input("Digite o cargo do novo funcionário: ")
    departamento_novo_funcionario = input("Digite o departamento do novo funcionário: ")

    cursor.execute(f'''
    INSERT INTO "Funcionario"
    VALUES(DEFAULT, '{nome_novo_funcionario}', '{salario_novo_funcionario}', '{cargo_novo_funcionario}', '{departamento_novo_funcionario}')
    ''')

    conn.commit()
    print("Funcionáio inserido!")

def inserir_departamento():
    print("Você está cadastrando um departamento. ")

    nome_novo_departamento = input("Digite o nome do novo departamento: ")

    cursor.execute(f'''
    INSERT INTO "Departamento"
    VALUES(DEFAULT, '{nome_novo_departamento}')
    ''')

    conn.commit()

    print("Departamento inserido.")

while True:
    try:

        print('''
        Bem vindo ao Gerenciamento XYZ:

        Escolha uma opção do menu:

        1 - Ver Funcionários
        2 - Ver Departamentos
        3 - Inserir Funcionários
        4 - Inserir Departamento
        0 - Sair

        ''')

        op = input("Digite a opção escolhida: ")

        match op:
            case "1":
                ver_funcionario()
            case "2":
                ver_departamento()
            case "3":
                inserir_funcionario()
            case "4":
                inserir_departamento()
            case "0":
                print("Saindo do programa...")
                cursor.close()
                conn.close()
                break
            case _:
                print("Opção inválida. Digite novamente!")

        input("Tecle enter para continuar.")

    except(Exception, psycopg2.Error) as error:
        print("Ocorreu um erro!", error)