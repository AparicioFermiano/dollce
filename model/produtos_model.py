# -*- coding: utf-8 -*-
from model.server import Conexao


class ProdutosModel():
    """Model de produtos."""
    def __init__(self):
        """Construtor."""
        self.con = Conexao('localhost', 'dollce', 'aparicio', '@Aparicio129')

    def realizar_conexao(self, sql):
        """."""
        dados = []
        try:
            dados = self.con.consultar(sql)
        except Exception as err: 
            raise Exception("Problemas no banco! %s ." % err)
        return dados

    def buscar_produtos(self, id_produto=None):
        """Busca os produtos."""
        sql = """
                SELECT * FROM vendas v
                INNER JOIN produtos p ON v.id_produto = p.id_produto
                INNER JOIN produto_detalhes pd ON pd.id_detalhe = p.id_detalhe
            """
        if id_produto:
            sql = sql + "where p.id_produto = %s " % id_produto
        produto = self.realizar_conexao(sql)
        return produto

    def buscar_imagens(self, id_produto=None):
        """."""
        sql = """
                SELECT
                    id_imagem, url_imagem, destaque, descricao 
                FROM produto_imagens WHERE id_produto = %s
                ORDER BY destaque DESC
            """ % id_produto
        imagens = self.realizar_conexao(sql)
        return imagens
