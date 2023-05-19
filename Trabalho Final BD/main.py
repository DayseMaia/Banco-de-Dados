import psycopg2                             #   Importando biblioteca para conexão com o Banco de Dados;
import clientes                             #   Importando arquivo clientes;
import produtos                             #   Importando arquivo produtos;
import compras                              #   Importando arquivo compras;

conn = psycopg2.connect(                    #   Criando conexão com o Banco de Dados;
    host = "localhost",
    database = "Farmacia",
    user = "postgres",
    password = "postgres"
)

cur = conn.cursor()                         #   Criando cursor;

def main():                                 #   Função main que abrange o menu principal;
    while True:

        print('''
    
    Bem vindo a Ninho Farma!!!

    ======================================
                MENU PRINCIPAL            
    ======================================
    
    [1] - Menu Clientes
    [2] - Menu Produtos
    [3] - Menu Compras
    [0] - Sair
    
    ''')

        opcao = input("Escolha a opção que deseja acessar: ")

        match opcao:
            case "1":
                clientes.menu_clientes()
            case "2":
                produtos.menu_produtos()
            case "3":
                compras.menu_compras()
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
