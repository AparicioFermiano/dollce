# -*- coding: utf-8 -*-
from model.server import Conexao


class ProdutosModel():
    """Model de produtos."""
    def __init__(self):
        """Construtor."""
        self.con = Conexao('localhost', 'dollce', 'aparicio', '@Aparicio129')

    def buscar_produtos(self, id_produto=None):
        """Busca os produtos."""
        if id_produto:
            sql = "select * from produtos where id_produto = %s " % id_produto
        else:
            sql = "select * from produtos"
        produto = []
        produto = self.con.consultar(sql)
        try:
            produto = self.con.consultar(sql)
        except Exception as err:
            msg = "Problemas no banco! %s ." % err
            raise Exception(msg)
        return produto
