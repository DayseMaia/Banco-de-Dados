import psycopg2                             #   Importando biblioteca para conexão com o Banco de Dados;
from prettytable import PrettyTable         #   Importando biblioteca que imprime tabelas;
from os import system                       #   Importando biblioteca que permite limpar o terminal a cada função executada;

conn = psycopg2.connect(                    #   Criando conexão com o Banco de Dados;
    host = "localhost",
    database = "Biblioteca",
    user = "postgres",
    password = "postgres"
)

cur = conn.cursor()                         #   Criando cursor;


def menu_livros():                          #   Função Menu Livros;
    system('cls')
    while True:
        
        print('''
        ===================================
                    MENU LIVROS            
        ===================================

        [1] - Lista de Livros
        [2] - Cadastrar Novo Livro
        [3] - Atualizar Livro
        [4] - Remover Livro
        [0] - Voltar ao menu principal
        
        ''')
        
        opcao = input("Escolha a opção que deseja acessar: ")
        
        match opcao:
            case "1":
                mostrar_livros()
            case "2":
                cadastrar_livro()
            case "3":
                atualizar_livro()
            case "4":
                remover_livro()
            case "0":
                system('cls')
                print('-'*60)
                print("Voltando ao menu principal...")
                print('-'*60)
                break
            case _:
                print('-'*60)
                print("Opção inválida. Escolha uma opção válida.")
                print('-'*60)

        input("Digite Enter para continuar...")
        system('cls')

def mostrar_livros():                     #   Função que lista os Livros cadastrados;
    system('cls')
    cur.execute('''
    SELECT * FROM "Livros"
    ORDER BY "ID_Livro"
    ''')

    colunas = [desc[0] for desc in cur.description]

    linhas = cur.fetchall()

    tabela = PrettyTable(colunas)
    for linha in linhas:
        tabela.add_row(linha)

    print(''' 
                    - Lista de Livros - 
    ''')
    print(tabela)


def cadastrar_livro():                    #   Função para cadastrar novo livro;
    system('cls')
    print(''' 
    - Cadastro de Livro: 
    ''')

    nome = input("Digite o nome do Livro: ")
    autor = input("Digite o autor do Livro: ")

    cur.execute(f'''
    INSERT INTO "Livros"
    VALUES(DEFAULT, '{nome}', '{autor}')
    ''')
    conn.commit()

    print('-'*60)
    print(f"O livro {nome} foi cadastrado com sucesso.")
    print('-'*60)


def atualizar_livro():                    #   Função para atualizar livro cadastrado;
    system('cls')
    print(''' 
    - Atualizar Livro: 
    ''')
    
    mostrar_livros()
    print()
    livro_escolhido = input("Digite o ID do livro: ")
    novo_nome = input("Digite o novo nome do livro (digite Enter para não alterar): ")
    novo_autor = input("Digite o novo autor do livro (digite Enter para não alterar): ")

    if novo_nome:
        cur.execute(f'''
        UPDATE "Livros"
        SET "Nome_Livro" = '{novo_nome}'
        WHERE "ID_Livro" = {livro_escolhido}
        ''')
        conn.commit()

    if novo_autor:
        cur.execute(f'''
        UPDATE "Livros"
        SET "Autor" = '{novo_autor}'
        WHERE "ID_Livro" = {livro_escolhido}
        ''')
        conn.commit()
    
    print('-'*60)
    print("Alteração realizada com sucesso!")
    print('-'*60)


def remover_livro():                      #   Função para remover Livro cadastrado;
    system('cls')
    print(''' 
    - Remover Livro: 
    ''')
    
    mostrar_livros()
    print()
    livro_escolhido = input("Digite o ID do livro: ")

    confirmar = input("Deseja mesmo remover este livro? (S/N) ").upper()

    match confirmar:
        case "S":
            cur.execute(f'''
            DELETE FROM "Livros"
            WHERE "ID_Livro" = '{livro_escolhido}'
            ''')
            conn.commit()
           
            print('-'*60)
            print("Livro removido com sucesso.")
            print('-'*60)

        case "N":
            print('-'*60)
            print("Voltando ao menu.")
            print('-'*60)

        case _:
            print('-'*60)
            print("Opção inválida. Voltando ao menu.")
            print('-'*60)