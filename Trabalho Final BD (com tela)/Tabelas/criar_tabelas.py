import psycopg2                             #Biblioteca para conexão com o Banco de Dados;

class Conexao:                              #Classe Conexão para definir a conexão com o banco;

    def __init__(self, dbname, host, port, user, password):
        self._dbname = dbname
        self._host = host
        self._port = port
        self._user = user
        self._password = password

    def criar_tabelas(self):                #Método para criar tabelas no banco de dados;
        try:
            con = psycopg2.connect(dbname=self._dbname, host=self._host, port = self._port, user = self._user, password = self._password)
            
            cursor = con.cursor()           #Criando cursor;
                                            #Criando tabela Clientes;
            cursor.execute("""
            CREATE TABLE "Clientes" (
            "ID_Cliente" SERIAL PRIMARY KEY,
            "Nome_Cliente" VARCHAR(255) NOT NULL,
            "CPF" CHAR(11) UNIQUE NOT NULL,
            "Email" VARCHAR(255) DEFAULT 'Não informado',
            "Telefone" VARCHAR(255) DEFAULT 'Não inforrmado',
            "Status" VARCHAR(255) DEFAULT 'Ativo'
            )
            """)
            print("Tabela criada com sucesso!")
                                            #Criando tabela Produtos;
            cursor.execute("""
            CREATE TABLE "Produtos" (
            "ID_Produto" SERIAL PRIMARY KEY,
            "Nome_Produto" VARCHAR(255) NOT NULL,
            "Valor_Produto" NUMERIC(10,2) NOT NULL,
            "Estoque_Produto" INT NOT NULL
            )
            """)
            print("Tabela criada com sucesso!")
                                            #Criando tabela Compras;
            cursor.execute("""
            CREATE TABLE "Compras" (
            "ID_Compra" SERIAL PRIMARY KEY,
            "ID_Cliente" INTEGER REFERENCES "Clientes"("ID_Cliente"),
            "ID_Produto" INTEGER REFERENCES "Produtos"("ID_Produto"),
            "Quantidade" INT NOT NULL,
            "Valor_Total" NUMERIC(10,2) NOT NULL,
            "Data_da_Venda" TIMESTAMP DEFAULT CURRENT_TIMESTAMP(0)
            )
            """)
            print("Tabela criada com sucesso!")
            
            con.commit()
            
            cursor.close()

            con.close()

            return True
        
        except(Exception, psycopg2.Error) as error:
            print("Ocorreu um erro:", error)

            return False
        
conexao_banco = Conexao("Farmacia", "localhost", "5432", "postgres", "postgres")

Conexao.criar_tabelas(conexao_banco)