#Cenário: Biblioteca

# Construir um sistema de cadastro de aluguéis de livros.

# - Deve conter um banco com as seguintes tabelas: Clientes, Aluguéis e Livros
# - Deve conter as seguintes funcionalidades: Cadastro de Clientes, Cadastro de Aluguéis, Cadastro de Livros e Visualização dos dados das 3 tabelas.

#Requisitos:
#   - Deve utilizar chave estrangeira

import psycopg2                             #   Importando biblioteca para conexão com o Banco de Dados;
import clientes                             #   Importando arquivo clientes;
import alugueis                             #   Importando arquivo alugueis;
import livros                               #   Importando arquivo livros;

conn = psycopg2.connect(                    #   Criando conexão com o Banco de Dados;
    host = "localhost",
    database = "Biblioteca",
    user = "postgres",
    password = "postgres"
)

cur = conn.cursor()                         #   Criando cursor;

def main():                                 #   Função main que abrange o menu principal;
    while True:

        print('''
    
    Bem vindo a Biblioteca XYZ!!!

    ======================================
                MENU PRINCIPAL            
    ======================================
    
    [1] - Menu Clientes
    [2] - Menu Livros
    [3] - Menu Alugueis
    [0] - Sair
    
    ''')

        opcao = input("Escolha a opção que deseja acessar: ")

        match opcao:
            case "1":
                clientes.menu_clientes()
            case "2":
                livros.menu_livros()
            case "3":
                alugueis.menu_alugueis()
            case "0":
                print('-'*60)
                print("Saindo da aplicação...")
                print('-'*60)
                cur.close()
                conn.close()
                break
            case _:
                print("Opção inválida! Escolha uma opção válida.")

if __name__ == "__main__":                  #   Chamando a função main para rodar o programa.
    main()
