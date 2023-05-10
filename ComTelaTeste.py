import PySimpleGUI as sg
import psycopg2


conn = psycopg2.connect(
    host="localhost",
    database="Farmacia",
    user="postgres",
    password="postgres"
)

cur = conn.cursor()

def menu_clientes():
    layout = [
        [sg.Text("Menu Clientes:")],
        [sg.Button('Ver lista de Clientes'), sg.Button('Cadastrar Novo Cliente')],
        [sg.Button('Atualizar Cliente'), sg.Button('Remover Cliente')],
        [sg.Button('Ver Clientes Inativos'), sg.Button('Voltar')],
    ]
    
    window = sg.Window('Farmácia XYZ - Menu Clientes', layout)
    
    while True:
        event, values = window.read()

        if event == 'Ver lista de Clientes':
            mostrar_clientes()
        elif event == 'Cadastrar Novo Cliente':
            cadastrar_cliente()
        elif event == 'Atualizar Cliente':
            atualizar_cliente()
        elif event == 'Remover Cliente':
            remover_cliente()
        elif event == 'Ver Clientes Inativos':
            mostrar_clientes_inativos()
        elif event == 'Voltar':
            break
    
    window.close()

def mostrar_clientes():
    cur.execute('''
    SELECT * FROM "Clientes"
    WHERE "Status" = 'Ativo'
    ORDER BY "ID_Cliente"
    ''')

    colunas = [desc[0] for desc in cur.description]

    linhas = cur.fetchall()

    data = []
    for linha in linhas:
        data.append(list(linha))

    layout = [
        [sg.Table(values=data, headings=colunas, max_col_width=25, background_color='#F7F3EC', auto_size_columns=True,
                  justification='center', num_rows=min(len(data), 20), text_color='black')],
        [sg.Button('Voltar ao menu Clientes')]
    ]

    window = sg.Window('Farmácia XYZ - Lista de Clientes', layout)

    while True:
        event, values = window.read()

        if event == 'Voltar ao menu Clientes':
            break

    window.close()


def cadastrar_cliente():
    # Implemente aqui o código para cadastrar um novo cliente
    pass

def atualizar_cliente():
    # Implemente aqui o código para atualizar um cliente existente
    pass

def remover_cliente():
    # Implemente aqui o código para remover um cliente
    pass

def mostrar_clientes_inativos():
    # Implemente aqui o código para mostrar a lista de clientes inativos
    pass

################################### PRODUTOS ###################################

def menu_produtos():
    layout = [
        [sg.Text("Menu Produtos:")],
        [sg.Button('Ver lista de Produtos'), sg.Button('Cadastrar Novo Produto')],
        [sg.Button('Atualizar Produto'), sg.Button('Remover Produto')],
        [sg.Button('Voltar')],
    ]
    
    window = sg.Window('Farmácia XYZ - Menu Produtos', layout)
    
    while True:
        event, values = window.read()

        if event == 'Ver lista de Produtos':
            mostrar_produtos()
        elif event == 'Cadastrar Novo Produto':
            cadastrar_produto()
        elif event == 'Atualizar Produto':
            atualizar_produto()
        elif event == 'Remover Produto':
            remover_produto()
        elif event == 'Voltar':
            break
    
    window.close()

def mostrar_produtos():
    # Implemente aqui o código para mostrar a lista de clientes
    pass

def cadastrar_produto():
    # Implemente aqui o código para cadastrar um novo cliente
    pass

def atualizar_produto():
    # Implemente aqui o código para atualizar um cliente existente
    pass

def remover_produto():
    # Implemente aqui o código para remover um cliente
    pass

################################### COMPRAS ###################################

def menu_compras():
    layout = [
        [sg.Text("Menu Compras:")],
        [sg.Button('Ver lista de Compras'), sg.Button('Cadastrar Nova Compra')],
        [sg.Button('Atualizar Compra'), sg.Button('Remover Compra')],
        [sg.Button('Voltar')],
    ]
    
    window = sg.Window('Farmácia XYZ - Menu Compras', layout)
    
    while True:
        event, values = window.read()

        if event == 'Ver lista de Compras':
            mostrar_compras()
        elif event == 'Cadastrar Nova Compra':
            cadastrar_compra()
        elif event == 'Atualizar Compra':
            atualizar_compra()
        elif event == 'Remover Compra':
            remover_compra()
        elif event == 'Voltar':
            break
    
    window.close()

def mostrar_compras():
    pass

def cadastrar_compra():
    pass

def atualizar_compra():
    pass

def remover_compra():
    pass

def main():
    while True:
        layout = [
            [sg.Text("Bem vindo a Farmácia XYZ")],
            [sg.Button('Menu Clientes'), sg.Button('Menu Produtos'), sg.Button('Menu Compras'), sg.Button('Sair')],
        ]
        
        window = sg.Window('Farmácia XYZ', layout)

        event, values = window.read()

        if event == 'Menu Clientes':
            menu_clientes()
        elif event == 'Menu Produtos':
            menu_produtos()
        elif event == 'Menu Compras':
            menu_compras()
        elif event == 'Sair':
            cur.close()
            conn.close()
            break

        window.close()

if __name__ == "__main__":
    main()
