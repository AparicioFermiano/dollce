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

    def buscar_produtos(self):
        """Busca o produto."""
        sql = """
            SELECT 
                p.id_produto,
                p.produto,
                pd.descricao,
                pd.dt_criacao,
                pd.dt_alteracao,
                v.vestuario
            FROM produtos p
                INNER JOIN produto_detalhes pd ON p.id_detalhe = pd.id_detalhe
                INNER JOIN vestuario v ON v.id_vestuario = pd.id_vestuario
        """
        produto = self.realizar_conexao(sql)
        return produto

    def buscar_produtos_card(self):
        """Busca os produtos para fazer o card."""
        sql = """
            SELECT 
                v.id_produto,
                v.preco,
                v.preco_promocao,
                v.parcelamento,
                v.preco_parcelado,
                p.id_produto,
                p.id_detalhe,
                p.produto,
                pi.url_imagem as imagem_principal,
                pi.descricao as descricao_principal,
                pi2.url_imagem as imagem_secundaria,
                pi2.descricao as descricao_secundaria
            FROM vendas v
                INNER JOIN produtos p ON v.id_produto = p.id_produto
                INNER JOIN produto_imagens pi ON pi.id_produto = p.id_produto and pi.destaque = True
                INNER JOIN produto_imagens pi2 ON pi2.id_produto = p.id_produto and pi2.secundaria = True
        """
        if id_produto:
            sql = sql + "where p.id_produto = %s " % id_produto
        produto = self.realizar_conexao(sql)
        return produto

    def buscar_produto_detalhes(self, id_produto):
        """Busca os detalhes do produto."""
        sql = """
            SELECT 
                *
            FROM vendas v
                INNER JOIN produtos p ON v.id_produto = p.id_produto
                INNER JOIN produto_detalhes pd ON p.id_detalhe = pd.id_detalhe
            WHERE p.id_produto = %s
        """ % id_produto
        produto = self.realizar_conexao(sql)
        return produto

    def buscar_produtos_cores(self, id_detalhe):
        """Busca as cores relacionada ao produto."""
        sql = """
            SELECT 
                c.id_cor,
                c.cor,
                c.hex
            FROM produtos p
            INNER JOIN cor c ON c.id_cor = p.id_cor 
            WHERE id_detalhe = %s
        """ % id_detalhe
        cores = self.realizar_conexao(sql)
        return cores

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
