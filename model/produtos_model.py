# -*- coding: utf-8 -*-
from model.server import Conexao


class ProdutosModel():
    """Model de produtos."""
    def __init__(self):
        """Construtor."""
        self.con = Conexao('localhost', 'dollce', 'aparicio', '@Aparicio129')

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
        produto = self.con.consultar(sql)
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
        produto = self.con.consultar(sql)
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
        produto = self.con.consultar_unit(sql)
        return produto

    def buscar_produtos_cores(self, id_produto):
        """Busca as cores relacionada ao produto."""
        sql = """
            SELECT
                pc.id_produto, 
                pc.id_cor,
                c.cor,
                c.hex
            FROM produto_cor pc
            INNER JOIN cor c ON c.id_cor = pc.id_cor 
            WHERE id_produto = %s
        """ % id_produto
        cores = self.con.consultar(sql)
        return cores

    def buscar_imagens(self, id_produto=None):
        """Busca as imagens relacionada ao produto."""
        sql = """
            SELECT
                id_imagem, url_imagem, destaque, descricao 
            FROM produto_imagens WHERE id_produto = %s
            ORDER BY destaque DESC
        """ % id_produto
        imagens = self.con.consultar(sql)
        return imagens

    def buscar_cores(self):
        """Busca as cores para ser listadas."""
        sql = "SELECT * FROM cor"
        cores = self.con.consultar(sql)
        return cores

    def buscar_categorias(self, id_vestuario=None):
        """Busca as categorias para ser listadas."""
        sql = """
            SELECT * FROM categoria
        """
        if id_vestuario:
            sql = sql + "where id_vestuario=%s" % id_vestuario
        categoria = self.con.consultar(sql)
        return categoria

    def buscar_vestuario(self):
        """."""
        sql = "SELECT * FROM vestuario"
        vestuario = self.con.consultar(sql)
        return vestuario

    def manipular_produto(
            self, id_produto, id_detalhe, produto, desc_produto, vestuario,
            categoria, resumo, url_mercado_livre, url_shopee,
            modelo, material, composicao, tamanhos, cores):
        """Faz a manipulacao do produto."""
        retorno = False
        if id_produto:
            sql_detalhes = """
                UPDATE produtos SET 
                    produto = '%s'
                WHERE id_produto = %i
            """ % (produto, int(id_produto))

            sql_produto = """
                UPDATE produto_detalhes SET 
                    descricao = '%(descricao)s',
                    id_categoria = %(id_categoria)i,
                    id_vestuario = %(id_vestuario)i,
                    id_genero = 1,
                    dt_alteracao = CURRENT_DATE,
                    url_mercado_livre = '%(url_mercado_livre)s',
                    url_shopee = '%(url_shopee)s',
                    resumo = '%(resumo)s',
                    modelo = '%(modelo)s',
                    material = '%(material)s',
                    composicao = '%(composicao)s'
                WHERE id_detalhe = %(id_detalhe)i
            """ % {
                "descricao": desc_produto, 
                "id_categoria": int(categoria), 
                "id_vestuario": int(vestuario),
                "url_mercado_livre": url_mercado_livre,
                "url_shopee": url_shopee,
                "resumo": resumo,
                "modelo": modelo,
                "material": material,
                "composicao": composicao,
                "id_detalhe": int(id_detalhe)}

            self.manipular_cores(id_produto=id_produto, cores=cores)
        else:
            # Sera feito um insert
            retorno = True

            sql_detalhes = """
                INSERT INTO produto_detalhes(
                    descricao, id_categoria, dt_criacao, 
                    id_vestuario, id_genero, url_mercado_livre, 
                    url_shopee, resumo, modelo, material, composicao) 
                VALUES(
                    '%s', %i, CURRENT_DATE, %i, 1, '%s', '%s', '%s',
                '%s', '%s', '%s')
                RETURNING(id_detalhe)
                """ % (desc_produto, int(categoria), int(vestuario), 
                    url_mercado_livre, url_shopee, resumo, modelo, 
                    material, composicao)
            
            sql_produto = """
                INSERT INTO produtos VALUES(default, '%s', %i, 100)
                RETURNING(id_produto)
            """ % (produto, id_detalhe)

        id_detalhe = self.con.manipular(sql_detalhes, retorno=retorno)

        id_produto = self.con.manipular(sql_produto, retorno=retorno)
        
        return id_produto

    def manipular_cores(self, id_produto, cores):
        """Faz a manipulacao das cores de um produto."""
        cores_old = self.buscar_produtos_cores(id_produto=id_produto)
        
        id_cores_old = []

        for c in cores_old:
            id_cores_old.append(int(c['id_cor']))

        sql_delete = """
            DELETE 
                produto_cor 
            WHERE 
                id_produto=%i AND id_cor=%i
        """

        for cor_old in id_cores_old:
            if cor_old not in map(int, cores):
                sql_cores = sql_delete % (int(id_produto), int(cor_old))
                self.con.manipular(sql_cores, retorno=False)

        sql_insert = """INSERT INTO produto_cor VALUES(%i, %i)"""

        for cor in cores:
            if int(cor) not in id_cores_old:
                sql_cores = sql_insert % (int(id_produto), int(cor))
                self.con.manipular(sql_cores, retorno=False)