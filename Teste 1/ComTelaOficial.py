import PySimpleGUI as sg
import psycopg2
import emoji

conn = psycopg2.connect(
    host="localhost",
    database="Farmacia",
    user="postgres",
    password="postgres"
)

cur = conn.cursor()

def menu_clientes():
    layout = [
        [sg.Text("Menu Clientes", font=('Arial', 14, 'bold'))],
        [sg.Button('Lista de Clientes', size=(20, 2), button_color=('white', '#4e8cff')), sg.Button('Cadastrar Novo Cliente', size=(20, 2), button_color=('white', '#4e8cff'))],
        [sg.Button('Atualizar Cliente', size=(20, 2), button_color=('white', '#4e8cff')), sg.Button('Remover Cliente', size=(20, 2), button_color=('white', '#4e8cff'))],
        [sg.Button('Lista de Clientes Inativos', size=(20, 2), button_color=('white', '#4e8cff')), sg.Button('Menu Principal', size=(20, 2), button_color=('white', '#e74c3c'))],
    ]
    
    window = sg.Window('Farmácia NinhoFarma', layout, size=(380, 200))
    
    while True:
        event, values = window.read()

        if event == 'Lista de Clientes':
            mostrar_clientes()
        elif event == 'Cadastrar Novo Cliente':
            cadastrar_cliente()
        elif event == 'Atualizar Cliente':
            atualizar_cliente(cur)
        elif event == 'Remover Cliente':
            remover_cliente()
        elif event == 'Lista de Clientes Inativos':
            mostrar_clientes_inativos()
        elif event == 'Menu Principal' or event == sg.WINDOW_CLOSED:
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
        [sg.Text('Lista de Clientes', font=('Arial', 14, 'bold'))],
        [sg.Table(values=data, headings=colunas, max_col_width=25, background_color='#F7F3EC', auto_size_columns=True,
                  justification='center', num_rows=min(len(data), 20), text_color='black')],
        [sg.Button('Voltar ao menu Clientes', size=(20, 2), button_color=('white', '#e74c3c'))]
    ]

    window = sg.Window('Farmácia NinhoFarma', layout)

    while True:
        event, values = window.read()

        if event == 'Voltar ao menu Clientes' or event == sg.WINDOW_CLOSED:
            break

    window.close()

def cadastrar_cliente():
    layout = [
        [sg.Text('Cadastro de Cliente', font=('Arial', 14, 'bold'))],
        [sg.Text('Nome: *', font=('Arial', 10, 'bold'))], 
        [sg.Input(key='nome')],
        [sg.Text('CPF (somente números): *', font=('Arial', 10, 'bold'))], 
        [sg.Input(key='cpf')],
        [sg.Text('Email:', font=('Arial', 10, 'bold'))], 
        [sg.Input(key='email')],
        [sg.Text('Telefone:', font=('Arial', 10, 'bold'))], 
        [sg.Input(key='telefone')],
        [sg.Text('Preenchimento obrigatório (*)', font=('Arial', 10, 'bold'))],
        [sg.Button('Cadastrar', button_color=('white', '#4e8cff')), sg.Button('Cancelar', button_color=('white', '#e74c3c'))]
    ]

    window = sg.Window('Farmácia NinhoFarma', layout)

    while True:
        event, values = window.read()

        if event == 'Cadastrar':
            nome = values['nome']
            cpf = values['cpf']
            email = values['email']
            telefone = values['telefone']

            if len(cpf) == 11 and cpf.isnumeric():
                if email == "" and telefone == "":
                    cur.execute(f'''
                    INSERT INTO "Clientes"
                    VALUES(DEFAULT, '{nome}', '{cpf}', DEFAULT, DEFAULT)
                    ''')
                    conn.commit()
                else:
                    cur.execute(f'''
                    INSERT INTO "Clientes"
                    VALUES(DEFAULT, '{nome}', '{cpf}', '{email}', '{telefone}')
                    ''')
                    conn.commit()

                sg.Popup(f"O cliente {nome} foi cadastrado com sucesso.\n", font=('Arial', 10, 'bold'), title="Cadastro de Cliente")
                break
            else:
                sg.Popup('''
CPF inválido!

O CPF deve conter 11 dígitos e ter somente números.
''', font=('Arial', 10, 'bold'), 
                title="CPF inválido!")
        elif event == 'Cancelar' or event == sg.WINDOW_CLOSED:
            break

    window.close()

def atualizar_cliente(cur):
    layout = [
        [sg.Text('Atualizar Cliente', font=('Arial', 14, 'bold'))],
        [sg.Text('Clientes:', font=('Arial', 12, 'bold'))],
        [sg.Listbox(values=get_clientes(cur), size=(30, 4), key='clientes')],
        [sg.Button('Selecionar', button_color=('white', '#4e8cff'))],
        [sg.Text('Novo Nome:')], 
        [sg.Input(key='novo_nome')],
        [sg.Text('Novo CPF:')], 
        [sg.Input(key='novo_cpf')],
        [sg.Text('Novo Email:')], 
        [sg.Input(key='novo_email')],
        [sg.Text('Novo Telefone:')], 
        [sg.Input(key='novo_telefone')],
        [sg.Button('Atualizar'), sg.Button('Cancelar')]
    ]

    window = sg.Window('Farmácia XYZ - Atualizar Cliente', layout)

    while True:
        event, values = window.read()

        if event == 'Selecionar':
            cliente_escolhido = values['clientes'][0].split(' - ')[0]
            ver_cliente_especifico(cliente_escolhido, cur)
        elif event == 'Atualizar':
            cliente_escolhido = values['clientes'][0].split(' - ')[0]
            novo_nome = values['novo_nome']
            novo_cpf = values['novo_cpf']
            novo_email = values['novo_email']
            novo_telefone = values['novo_telefone']

            if novo_nome:
                cur.execute(f'''
                UPDATE "Clientes"
                SET "Nome_Cliente" = '{novo_nome}'
                WHERE "ID_Cliente" = {cliente_escolhido}
                ''')
                conn.commit()

            if novo_cpf:
                cur.execute(f'''
                UPDATE "Clientes"
                SET "CPF" = '{novo_cpf}'
                WHERE "ID_Cliente" = {cliente_escolhido}
                ''')
                conn.commit()

            if novo_email:
                cur.execute(f'''
                UPDATE "Clientes"
                SET "Email" = '{novo_email}'
                WHERE "ID_Cliente" = {cliente_escolhido}
                ''')
                conn.commit()

            if novo_telefone:
                cur.execute(f'''
                UPDATE "Clientes"
                SET "Telefone" = '{novo_telefone}'
                WHERE "ID_Cliente" = {cliente_escolhido}
                ''')
                conn.commit()

            sg.Popup("Alteração realizada com sucesso!")
            break
        elif event == 'Cancelar':
            break

    window.close()

def ver_cliente_especifico(id_cliente, cur):
    cur.execute(f'''SELECT * FROM "Clientes"
    WHERE "ID_Cliente" = {id_cliente}
    ORDER BY "ID_Cliente"
    ''')

    cliente = cur.fetchone()

    layout = [
        [sg.Text('- Cliente Escolhido -')],
        [sg.Text(f'ID: {cliente[0]}')],
        [sg.Text(f'Nome: {cliente[1]}')],
        [sg.Text(f'CPF: {cliente[2]}')],
        [sg.Text(f'Email: {cliente[3]}')],
        [sg.Text(f'Telefone: {cliente[4]}')],
        [sg.Button('Fechar')]
    ]

    window = sg.Window('Farmácia XYZ - Cliente Escolhido', layout)

    while True:
        event, _ = window.read()
        if event == 'Fechar':
            break

    window.close()


def remover_cliente():
    cur.execute('''
    SELECT * FROM "Clientes" 
    ORDER BY "ID_Cliente"
    ''')
    
    colunas = [desc[0] for desc in cur.description]
    linhas = cur.fetchall()
    tabela_clientes = [[str(cell) for cell in linha] for linha in linhas]

    layout = [
        [sg.Text('Lista de Clientes:')],
        [sg.Table(values=tabela_clientes, headings=colunas, key='tabela_cliente')],
        [sg.Button('Escolher Cliente'), sg.Button('Fechar')]
    ]

    window = sg.Window('Remover Cliente', layout)

    while True:
        event, values = window.read()

        if event == sg.WINDOW_CLOSED or event == 'Fechar':
            break
        elif event == 'Escolher Cliente':
            selecionar_linhas = values['tabela_cliente']
            if selecionar_linhas:
                cliente_escolhido = tabela_clientes[selecionar_linhas[0]][0]
                ver_cliente_espec_remover(cliente_escolhido)

                confirmar = sg.popup_yes_no('Deseja remover este cliente?')

                if confirmar == 'Yes':
                    cur.execute(f'''
                        UPDATE "Clientes"
                        SET "Status" = 'Inativo'
                        WHERE "ID_Cliente" = '{cliente_escolhido}'
                    ''')
                    conn.commit()
                    sg.popup('Cliente removido com sucesso.')
                else:
                    sg.popup('Operação cancelada.')
            else:
                sg.popup('Nenhum cliente selecionado.')

    window.close()


def ver_cliente_espec_remover(id_cliente):
    cur.execute(f'''SELECT * FROM "Clientes"
    WHERE "ID_Cliente" = {id_cliente}
    ORDER BY "ID_Cliente"
    ''')

    colunas = [desc[0] for desc in cur.description]
    linhas = cur.fetchall()

    tabela_clientes = [[str(cell) for cell in linha] for linha in linhas]

    cur.execute(f'''SELECT * FROM "Compras"
    WHERE "ID_Cliente" = {id_cliente}
    ORDER BY "ID_Compra"
    ''')

    colunas = [desc[0] for desc in cur.description]
    linhas = cur.fetchall()

    tabela_compras = [[str(cell) for cell in linha] for linha in linhas]

    layout = [
        [sg.Text('Cliente Escolhido:')],
        [sg.Table(values=tabela_clientes, headings=colunas)],
        [sg.Text('Compras do Cliente Escolhido:')],
        [sg.Table(values=tabela_compras, headings=colunas)],
        [sg.Button('Fechar')]
    ]

    window = sg.Window('Detalhes do Cliente', layout)

    while True:
        event, values = window.read()

        if event == sg.WINDOW_CLOSED or event == 'Fechar':
            break

    window.close()


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
            atualizar_produto(cur)
        elif event == 'Remover Produto':
            remover_produto()
        elif event == 'Voltar':
            break
    
    window.close()

def mostrar_produtos():
    cur.execute('''
    SELECT * FROM "Produtos"
    ORDER BY "ID_Produto"
    ''')

    colunas = [desc[0] for desc in cur.description]

    linhas = cur.fetchall()

    data = []
    for linha in linhas:
        data.append(list(linha))

    layout = [
        [sg.Table(values=data, headings=colunas, max_col_width=25, background_color='#F7F3EC', auto_size_columns=True,
                  justification='center', num_rows=min(len(data), 20), text_color='black')],
        [sg.Button('Voltar ao menu Produtos')]
    ]

    window = sg.Window('Farmácia XYZ - Lista de Produtos', layout)

    while True:
        event, values = window.read()
        if event == 'Voltar ao menu Produtos':
            break

    window.close()

def cadastrar_produto():
    layout = [
        [sg.Text('- Cadastro de Produtos -')],
        [sg.Text('Nome:'), sg.Input(key='nome')],
        [sg.Text('Valor:'), sg.Input(key='valor')],
        [sg.Text('Estoque:'), sg.Input(key='estoque')],
        [sg.Button('Cadastrar'), sg.Button('Cancelar')]
    ]

    window = sg.Window('Farmácia XYZ - Cadastro de Produtos', layout)

    while True:
        event, values = window.read()

        if event == 'Cadastrar':
            nome = values['nome']
            valor = values['valor']
            estoque = values['estoque']

            cur.execute(f'''
            INSERT INTO "Produtos"
            VALUES(DEFAULT, '{nome}', '{valor}', '{estoque}')
            ''')
            conn.commit()

            sg.Popup(f"O produto {nome} foi cadastrado com sucesso.", title="Cadastro de Produto")
            break
        elif event == 'Cancelar':
            break

    window.close()

#Atualizar produto

def atualizar_produto(cur):
    layout = [
        [sg.Text('- Atualizar Produto -')],
        [sg.Text('Produtos:')],
        [sg.Listbox(values=get_produtos(cur), size=(30,4), key='produtos')],
        [sg.Button('Selecionar')],
        [sg.Text('Novo Nome:'), sg.Input(key='novo_nome')],
        [sg.Text('Novo Valor:'), sg.Input(key='novo_valor')],
        [sg.Text('Novo Estoque:'), sg.Input(key='novo_estoque')],
        [sg.Button('Atualizar'), sg.Button('Cancelar')]
    ]

    window = sg.Window('Farmácia XYZ - Atualizar Produto', layout)

    while True:
        event, values = window.read()

        if event == sg.WINDOW_CLOSED or event == 'Cancelar':
            break

        if event == 'Selecionar':
            produto_escolhido = values['produtos'][0].split(' - ')[0]
            ver_produto_especifico(produto_escolhido, cur)
        
        if event == 'Atualizar':
            produto_escolhido = values['produtos'][0].split(' - ')[0]
            novo_nome = values['novo_nome']
            novo_valor = values['novo_valor']
            novo_estoque = values['novo_estoque']

            if novo_nome:
                cur.execute(f'''
                UPDATE "Produtos"
                SET "Nome_Produto" = '{novo_nome}'
                WHERE "ID_Produto" = {produto_escolhido}
                ''')
                conn.commit()

            if novo_valor:
                cur.execute(f'''
                UPDATE "Produtos"
                SET "Valor_Produto" = '{novo_valor}'
                WHERE "ID_Produto" = {produto_escolhido}
                ''')
                conn.commit()

            if novo_estoque:
                cur.execute(f'''
                UPDATE "Produtos"
                SET "Estoque_Produto" = '{novo_estoque}'
                WHERE "ID_Produto" = {produto_escolhido}
                ''')
                conn.commit()

            sg.Popup("Alteração realizada com sucesso!")
            break

    window.close()

def ver_produto_especifico(id_produto, cur):
    cur.execute(f'''SELECT * FROM "Produtos"
    WHERE "ID_Produto" = {id_produto}
    ORDER BY "ID_Produto"
    ''')

    produto = cur.fetchone()

    layout = [
        [sg.Text('- Produto Escolhido -')],
        [sg.Text(f'ID: {produto[0]}')],
        [sg.Text(f'Nome: {produto[1]}')],
        [sg.Text(f'Valor: {produto[2]}')],
        [sg.Text(f'Estoque: {produto[3]}')],
        [sg.Button('Fechar')]
    ]

    window = sg.Window('Farmácia XYZ - Produto Escolhido', layout)

    while True:
        event, _ = window.read()

        if event == 'Fechar':
            break

    window.close()


def remover_produto():
    # Implemente aqui o código para remover uma compra
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
            cadastrar_compra(cur)
        elif event == 'Atualizar Compra':
            atualizar_compra(cur)
        elif event == 'Remover Compra':
            remover_compra()
        elif event == 'Voltar':
            break
    
    window.close()

def mostrar_compras():
    cur.execute('''
    SELECT * FROM "Compras"
    ORDER BY "ID_Compra"
    ''')

    colunas = [desc[0] for desc in cur.description]

    linhas = cur.fetchall()

    data = []
    for linha in linhas:
        data.append(list(linha))

    layout = [
        [sg.Table(values=data, headings=colunas, max_col_width=25, background_color='#F7F3EC', auto_size_columns=True,
                  justification='center', num_rows=min(len(data), 20), text_color='black')],
        [sg.Button('Voltar ao menu Compras')]
    ]

    window = sg.Window('Farmácia XYZ - Lista de Compras', layout)

    while True:
        event, values = window.read()

        if event == 'Voltar ao menu Compras':
            break

    window.close()

def get_clientes(cur):
    cur.execute('''
    SELECT "ID_Cliente", "Nome_Cliente" FROM "Clientes"
    WHERE "Status" = 'Ativo'
    ORDER BY "ID_Cliente"
    ''')

    clientes = cur.fetchall()
    options = [f"{cliente[0]} - {cliente[1]}" for cliente in clientes]
    return options

def get_produtos(cur):
    cur.execute('''
    SELECT "ID_Produto", "Nome_Produto" FROM "Produtos"
    ORDER BY "ID_Produto"
    ''')

    produtos = cur.fetchall()
    options = [f"{produto[0]} - {produto[1]}" for produto in produtos]
    return options

def get_compras(cur):
    cur.execute('''
    SELECT "ID_Compra", "ID_Cliente" FROM "Compras"
    ORDER BY "ID_Compra"
    ''')

    compras = cur.fetchall()
    options = [f"{compra[0]} - {compra[1]}" for compra in compras]
    return options


def cadastrar_compra(cur):
    layout = [
        [sg.Text('- Cadastro de Compra -')],
        [sg.Text('Cliente:')],
        [sg.Listbox(values=get_clientes(cur), size=(30, 4), key='cliente')],
        [sg.Text('Produto:')],
        [sg.Listbox(values=get_produtos(cur), size=(30, 4), key='produto')],
        [sg.Text('Quantidade:'), sg.Input(key='quantidade')],
        [sg.Button('Cadastrar'), sg.Button('Cancelar')]
    ]

    window = sg.Window('Farmácia XYZ - Cadastro de Compra', layout)

    while True:
        event, values = window.read()

        if event == 'Cadastrar':
            cliente = values['cliente'][0].split(' - ')[0]
            produto = values['produto'][0].split(' - ')[0]
            quantidade = int(values['quantidade'])

            cur.execute(f'''
            SELECT "Valor_Produto", "Estoque_Produto" FROM "Produtos"
            WHERE "ID_Produto" = {produto}
            ''')
            
            result = cur.fetchone()
            valor_produto, estoque_produto = result[0], result[1]

            if quantidade > estoque_produto or estoque_produto == 0:
                sg.Popup("Produto sem estoque.")
            else:
                estoque_produto -= quantidade
                cur.execute(f'''
                UPDATE "Produtos"
                SET "Estoque_Produto" = {estoque_produto}
                WHERE "ID_Produto" = {produto}
                ''')
                conn.commit()
            
                valor_total = valor_produto * quantidade

                cur.execute(f'''
                INSERT INTO "Compras"
                VALUES(DEFAULT, '{cliente}', '{produto}', '{quantidade}', '{valor_total}', DEFAULT)
                ''')
                conn.commit()

                sg.Popup(f"Compra realizada com sucesso. Valor total da compra: {valor_total}")
                break
        elif event == 'Cancelar':
            break

    window.close()

def atualizar_compra(cur):
    layout = [
        [sg.Text('- Atualizar Compra -')],
        [sg.Text('Compras:')],
        [sg.Listbox(values=get_compras(cur), size=(30,4), key='compras')],
        [sg.Button('Selecionar')],
        [sg.Text('Novo ID Cliente:'), sg.Input(key='novo_id_cliente')],
        [sg.Text('Novo ID Produto:'), sg.Input(key='novo_id_produto')],
        [sg.Text('Nova quantidade:'), sg.Input(key='nova_quantidade')],
        [sg.Text("Novo valor total:"), sg.Input(key='novo_valor_total')],
        [sg.Button('Atualizar'), sg.Button('Cancelar')]
    ]

    window = sg.Window('Farmácia XYZ - Atualizar Compra', layout)

    while True:
        event, values = window.read()

        if event == sg.WINDOW_CLOSED or event == 'Cancelar':
            break

        if event == 'Selecionar':
            compra_escolhida = values['compras'][0].split(' - ')[0]
            ver_compra_especifica(compra_escolhida, cur)

        if event == 'Atualizar':
            compra_escolhida = values['compras'][0].split(' - ')[0]
            novo_id_cliente = values['novo_id_cliente']
            novo_id_produto = values['novo_id_produto']
            nova_quantidade = values['nova_quantidade']
            novo_valor_total = values['novo_valor_total']

            if novo_id_cliente:
                cur.execute(f'''
                UPDATE "Compras"
                SET "ID_Cliente" = '{novo_id_cliente}'
                WHERE "ID_Compra" = {compra_escolhida}
                ''')
                conn.commit()

            if novo_id_produto:
                cur.execute(f'''
                UPDATE "Compras"
                SET "ID_Produto" = '{novo_id_produto}'
                WHERE "ID_Compra" = {compra_escolhida}
                ''')
                conn.commit()

            if nova_quantidade:
                cur.execute(f'''
                UPDATE "Compras"
                SET "Quantidade" = '{nova_quantidade}'
                WHERE "ID_Compra" = {compra_escolhida}
                ''')
                conn.commit()

            if novo_valor_total:
                cur.execute(f'''
                UPDATE "Compras"
                SET "Valor_Total" = '{novo_valor_total}'
                WHERE "ID_Compra" = {compra_escolhida}
                ''')
                conn.commit()

            sg.Popup("Alteração realizada com sucesso!")
            break

    window.close()

def ver_compra_especifica(id_compra, cur):
    cur.execute(f'''SELECT * FROM "Compras"
    WHERE "ID_Compra" = {id_compra}
    ORDER BY "ID_Compra"
    ''')

    compra = cur.fetchone()

    layout = [
        [sg.Text('- Compra Escolhida -')],
        [sg.Text(f'ID Compra: {compra[0]}')],
        [sg.Text(f'ID Cliente: {compra[1]}')],
        [sg.Text(f'ID Produto: {compra[2]}')],
        [sg.Text(f'Quantidade: {compra[3]}')],
        [sg.Text(f'Valor Total: {compra[4]}')],
        [sg.Text(f'Data da venda: {compra[5]}')],
        [sg.Button('Fechar')]
    ]

    window = sg.Window('Farmácia XYZ - Compra Escolhida', layout)

    while True:
        event, _ = window.read()

        if event == 'Fechar':
            break

    window.close()

def remover_compra():
    pass

def main():
    sg.theme('DarkGrey5')

    while True:
        layout = [
            [sg.Text("Bem vindo a Farmácia XYZ")],
            [sg.Button(emoji.emojize(':busts_in_silhouette: Menu Clientes'), size=(20, 2), button_color=('white', '#4e8cff'), key='clientes')], 
            [sg.Button(emoji.emojize(':package: Menu Produtos'), size=(20, 2), button_color=('white', '#f5a742'), key='produtos')], 
            [sg.Button(emoji.emojize(':shopping_cart: Menu Compras'), size=(20, 2), button_color=('white', '#3dcf80'), key='compras')],
            [sg.Button('Sair', size=(10, 2), button_color=('white', '#e74c3c'))],
        ]
        
        window = sg.Window('Farmácia XYZ', layout)

        event, values = window.read()

        if event == 'clientes':
            menu_clientes()
        elif event == 'produtos':
            menu_produtos()
        elif event == 'compras':
            menu_compras()
        elif event == 'Sair' or event == sg.WINDOW_CLOSED:
            cur.close()
            conn.close()
            break

        window.close()

if __name__ == "__main__":
    main()