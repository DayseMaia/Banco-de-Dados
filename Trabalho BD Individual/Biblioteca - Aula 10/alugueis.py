import psycopg2                             #   Importando biblioteca para conexão com o Banco de Dados;
from prettytable import PrettyTable         #   Importando biblioteca que imprime tabelas;
import clientes                             #   Importando arquivo clientes;
import livros                               #   Importando arquivo livros;
from os import system                       #   Importando biblioteca que permite limpar o terminal a cada função executada;

conn = psycopg2.connect(                    #   Criando conexão com o Banco de Dados;
    host = "localhost",
    database = "Biblioteca",
    user = "postgres",
    password = "postgres"
)

cur = conn.cursor()                         #   Criando cursor;


def menu_alugueis():                        #   Função Menu Alugueis;
    system('cls')
    while True:
        
        print('''
        =====================================
                    MENU ALUGUEIS            
        =====================================

        [1] - Lista de Alugueis
        [2] - Cadastrar Nova Aluguel
        [3] - Atualizar Aluguel
        [4] - Remover Aluguel
        [0] - Voltar ao menu principal
        
        ''')
        
        opcao = input("Escolha a opção que deseja acessar: ")
        
        match opcao:
            case "1":
                mostrar_alugueis()
            case "2":
                cadastrar_aluguel(cur)
            case "3":
                atualizar_aluguel()
            case "4":
                remover_aluguel()
            case "0":
                system('cls')
                print('-'*60)
                print("Voltando ao menu principal...")
                print('-'*60)
                break
            case _:
                print('-'*60)
                print("Opção inválida! Escolha uma opção válida.")
                print('-'*60)

        input("Digite Enter para continuar...")
        system('cls')


def mostrar_alugueis():
    system('cls')
    cur.execute('''
    SELECT * FROM "Alugueis"
    ORDER BY "ID_Aluguel"
    ''')

    colunas = [desc[0] for desc in cur.description]

    linhas = cur.fetchall()

    tabela = PrettyTable(colunas)
    for linha in linhas:
        id_cliente = linha[1]
        id_livro = linha[2]

        # Consultar o nome do cliente com base no ID do cliente
        cur.execute(f'''
        SELECT "Nome_Cliente" FROM "Clientes"
        WHERE "ID_Cliente" = {id_cliente}
        ''')
        nome_cliente = cur.fetchone()[0]

        # Consultar o nome do produto com base no ID do livro
        cur.execute(f'''
        SELECT "Nome_Livro" FROM "Livros"
        WHERE "ID_Livro" = {id_livro}
        ''')
        nome_livro = cur.fetchone()[0]

        # Substituir o ID pelo nome do cliente e do livro
        linha = list(linha)
        linha[1] = nome_cliente
        linha[2] = nome_livro

        tabela.add_row(linha)

    print('''
                            - Lista de Alugueis - 
    ''')
    print(tabela)


def cadastrar_aluguel(cur):                  #   Função para cadastrar novo aluguel;
    system('cls')
    print(''' 
    - Cadastro de Aluguel: 
    ''')

    clientes.mostrar_clientes()
    print()
    cliente = input("Digite o ID do cliente: ")

    livros.mostrar_livros()
    print()
    livro = input("Digite o ID do livro: ")

    cur.execute(f'''
    INSERT INTO "Alugueis"
    VALUES(DEFAULT, '{cliente}', '{livro}', DEFAULT)
    ''')
    conn.commit()
    
    print('-'*60)
    print(f"Aluguel realizado com sucesso.")
    print('-'*60)


def atualizar_aluguel():                     #   Função para atualizar aluguel cadastrado;
    system('cls')
    print(''' 
    - Atualizar Aluguel: 
    ''')
    
    mostrar_alugueis()
    print()

    aluguel_escolhido = input("Digite o ID do aluguel: ")
    clientes.mostrar_clientes()
    novo_id_cliente = input("Digite o novo ID do cliente no aluguel (digite Enter para não alterar): ")
    livros.mostrar_livros()
    novo_id_livro = input("Digite o novo ID do livro no aluguel (digite Enter para não alterar): ")

    if novo_id_cliente:
        cur.execute(f'''
        UPDATE "Alugueis"
        SET "ID_Cliente" = {novo_id_cliente}
        WHERE "ID_Aluguel" = {aluguel_escolhido}
        ''')
        conn.commit()

    if novo_id_livro:
        cur.execute(f'''
        UPDATE "Alugueis"
        SET "ID_Livro" = {novo_id_livro}
        WHERE "ID_Alugueis" = {aluguel_escolhido}
        ''')
        conn.commit()

    print('-'*60)
    print("Alteração realizada com sucesso!")
    print('-'*60)


def remover_aluguel():                       #   Função para remover aluguel cadastrado;
    system('cls')
    print(''' 
    - Remover Aluguel: 
    ''')
    
    mostrar_alugueis()
    print()

    aluguel_escolhido = input("Digite o ID do aluguel: ")

    confirmar = input("Deseja mesmo remover essa aluguel? (S/N) ").upper()

    match confirmar:
        case "S":
            cur.execute(f'''
            DELETE FROM "Alugueis"
            WHERE "ID_Aluguel" = '{aluguel_escolhido}'
            ''')
            conn.commit()
           
            print('-'*60)
            print("Aluguel removido com sucesso.")
            print('-'*60)

        case "N":
            print('-'*60)
            print("Voltando ao menu.")
            print('-'*60)

        case _:
            print('-'*60)
            print("Opção inválida. Voltando ao menu.")
            print('-'*60)
