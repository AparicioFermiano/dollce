# -*- coding: utf-8 -*-
from model.server import Conexao


class ProdutosModel():
    """Model de produtos."""
    def __init__(self):
        """Construtor."""
        self.con = Conexao('localhost', 'dollce', 'aparicio', '@Aparicio129')

    def buscar_produtos(self, id_produto=None):
        """Busca os produtos."""
        sql = """
                select * from vendas v
                inner join produtos p on v.id_produto = p.id_produto
                inner join produto_detalhes pd on pd.id_detalhe = p.id_detalhe
            """
        if id_produto:
            sql = sql + "where id_produto = %s " % id_produto
        produto = []
        produto = self.con.consultar(sql)
        try:
            produto = self.con.consultar(sql)
        except Exception as err:
            msg = "Problemas no banco! %s ." % err
            raise Exception(msg)
        return produto
