from Controle.classConexao import Conexao
from Modelo.classCliente import Cliente
from Modelo.classProduto import Produto
from Modelo.classCompra import Compra
import psycopg2

conexaoBanco = Conexao("Loja", "localhost", "5432", "postgres", "postgres")
