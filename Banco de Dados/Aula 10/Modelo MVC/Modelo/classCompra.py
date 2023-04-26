class Compra:
    def __init__(self, idCompra, idCliente, idProduto, quantidade, valorTotal, timestamp):
        self._idCompra = idCompra
        self._idCliente = idCliente
        self._idProduto = idProduto
        self._quantidade = quantidade
        self._valorTotal = valorTotal
        self._timestamp = timestamp

