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
            "Status" VARCHAR(10) DEFAULT 'Ativo'
            )
            """)
            print("Tabela criada com sucesso!")
                                            #Criando tabela Livros;
            cursor.execute("""
            CREATE TABLE "Livros" (
            "ID_Livro" SERIAL PRIMARY KEY,
            "Nome_Livro" VARCHAR(255) NOT NULL,
            "Autor" VARCHAR(255) NOT NULL
            )
            """)
            print("Tabela criada com sucesso!")
                                            #Criando tabela Alugueis;
            cursor.execute("""
            CREATE TABLE "Alugueis" (
            "ID_Aluguel" SERIAL PRIMARY KEY,
            "ID_Cliente" INTEGER REFERENCES "Clientes"("ID_Cliente"),
            "ID_Livro" INTEGER REFERENCES "Livros"("ID_Livro"),
            "Data_do_Aluguel" TIMESTAMP DEFAULT CURRENT_TIMESTAMP(0)
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
        
conexao_banco = Conexao("Biblioteca", "localhost", "5432", "postgres", "postgres")

Conexao.criar_tabelas(conexao_banco)