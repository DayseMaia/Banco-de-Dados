import PySimpleGUI as sg
import psycopg2
import clientes
import produtos
import compras

conn = psycopg2.connect(
    host="localhost",
    database="Farmacia",
    user="postgres",
    password="postgres"
)

cur = conn.cursor()


def main():
    sg.theme('LightGrey1')

    while True:
        layout = [
            [sg.Text("Sistema de Gerenciamento NinhoFarma", font=('Arial', 14, 'bold'))],
            [sg.Text('')], 
            [sg.Button('📋  Menu Clientes', size=(20, 2), button_color=('white', '#304d63'), key='clientes'), sg.Button('🛒  Menu Produtos', size=(20, 2), button_color=('white', '#357599'), key='produtos'), sg.Button('💸  Menu Compras', size=(20, 2), button_color=('white', '#4e8cff'), key='compras')], 
            [sg.Text('')],
            [sg.Button('Sair', size=(10, 2), button_color=('white', '#e74c3c'))],
        ]
        
        window = sg.Window('Farmácia NinhoFarma', layout)

        event, _ = window.read()

        if event == 'clientes':
            clientes.menu_clientes()
        elif event == 'produtos':
            produtos.menu_produtos()
        elif event == 'compras':
            compras.menu_compras()
        elif event == 'Sair' or event == sg.WINDOW_CLOSED:
            cur.close()
            conn.close()
            break

        window.close()

if __name__ == "__main__":
    main()
