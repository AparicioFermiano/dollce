"""Model de Produtos."""
from Products.extensions.database import consultar, consultar_unit, manipular


class ProdutosModel():
    """Model de produtos."""

    def __init__(self):
        """."""

    def buscar_produtos(self):
        """Busca o produto."""
        sql = """
            SELECT
                p.id_produto,
                p.produto,
                p.id_detalhe,
                pd.descricao,
                pd.dt_criacao,
                pd.dt_alteracao,
                v.vestuario
            FROM produtos p
                INNER JOIN produto_detalhes pd ON p.id_detalhe = pd.id_detalhe
                INNER JOIN vestuario v ON v.id_vestuario = pd.id_vestuario
        """
        produto = consultar(sql)
        return produto

    def buscar_produtos_card(self):
        """Busca os produtos para fazer o card."""
        sql = """
            SELECT
                v.id_produto,
                v.preco,
                v.preco_promocao,
                v.parcelamento,
                p.id_produto,
                p.id_detalhe,
                p.produto,
                pi.url_imagem as imagem_principal,
                pi.descricao as descricao_principal,
                pi2.url_imagem as imagem_secundaria,
                pi2.descricao as descricao_secundaria
            FROM vendas v
                INNER JOIN produtos p ON v.id_produto = p.id_produto
                LEFT JOIN produto_imagens pi ON pi.id_produto = \
                p.id_produto and pi.destaque = True
                LEFT JOIN produto_imagens pi2 ON pi2.id_produto = \
                p.id_produto and pi2.secundaria = True
        """
        produto = consultar(sql)
        return produto

    def buscar_produto_detalhes(self, id_produto):
        """Busca os detalhes do produto."""
        sql = """
            SELECT
                p.id_produto,
                p.produto,
                p.id_detalhe,
                pd.descricao,
                pd.id_categoria,
                pd.id_colecao,
                pd.id_vestuario,
                pd.url_mercado_livre,
                pd.url_shopee,
                pd.composicao,
                pd.modelo,
                pd.material,
                pd.tamanho_p,
                pd.tamanho_m,
                pd.tamanho_g,
                pd.resumo,
                v.preco,
                v.preco_promocao,
                v.parcelamento
            FROM produtos p
                INNER JOIN produto_detalhes pd ON p.id_detalhe = pd.id_detalhe
                INNER JOIN vendas v ON p.id_produto = v.id_produto
            WHERE p.id_produto = %i
        """ % int(id_produto)
        produto = consultar_unit(sql)
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
        cores = consultar(sql)
        return cores

    def buscar_imagens(self, id_produto=None):
        """Busca as imagens relacionada ao produto."""
        sql = """
            SELECT
                id_imagem,
                url_imagem,
                ordem
            FROM produto_imagens WHERE id_produto = %s
            ORDER BY ordem DESC
        """ % id_produto
        imagens = consultar(sql)
        return imagens

    def buscar_cores(self):
        """Busca as cores para ser listadas."""
        sql = "SELECT * FROM cor"
        cores = consultar(sql)
        return cores

    def buscar_categorias(self, id_vestuario=None):
        """Busca as categorias para ser listadas."""
        sql = """
            SELECT * FROM categoria
        """
        if id_vestuario:
            sql = sql + "where id_vestuario=%s" % id_vestuario
        categoria = consultar(sql)
        return categoria

    def buscar_vestuario(self):
        """."""
        sql = "SELECT * FROM vestuario"
        vestuario = consultar(sql)
        return vestuario

    def manipular_imagem(
            self, id_produto, imagem_principal, imagem_secundaria,
            imagem_adicional1, imagem_adicional2):
        """Faz a manipulacao das imagens."""
        if id_produto:
            sql_imagem = """
                UPDATE
                    produto_imagens
                SET
                    url_imagem = '%s'
                WHERE
                    id_produto = %i AND
                    ordem = %i
            """

            if imagem_principal:
                manipular(sql_imagem % (imagem_principal, int(id_produto), 1))
            if imagem_secundaria:
                manipular(sql_imagem % (imagem_secundaria, int(id_produto), 2))
            if imagem_adicional1:
                manipular(sql_imagem % (imagem_adicional1, int(id_produto), 3))
            if imagem_adicional2:
                manipular(sql_imagem % (imagem_adicional2, int(id_produto), 4))
        else:
            sql_imagem = """
                INSERT INTO produto_imagens(
                    id_produto, url_imagem, dt_criacao, ordem)
                VALUES(
                    %i, '%s', CURRENT_DATE, %i)
            """

            manipular(sql_imagem % (int(id_produto), imagem_principal, 1))
            manipular(sql_imagem % (int(id_produto), imagem_secundaria, 2))
            manipular(sql_imagem % (int(id_produto), imagem_adicional1, 3))
            manipular(sql_imagem % (int(id_produto), imagem_adicional2, 4))

    def manipular_produto(
            self, id_produto, id_detalhe, produto, desc_produto, vestuario,
            categoria, resumo, url_mercado_livre, url_shopee, modelo,
            material, composicao, cores, tamanho_p, tamanho_m,
            tamanho_g, preco, preco_promocao, parcelamento):
        """Faz a manipulacao do produto."""
        if id_produto:
            sql_detalhes = """
                UPDATE produtos SET
                    produto = '%s'
                WHERE id_produto = %i
            """ % (produto, int(id_produto))

            sql_valor = """
                UPDATE vendas SET
                    preco = %(preco)d,
                    preco_promocao = %(preco_promocao)d,
                    parcelamento = %(parcelamento)i
                WHERE
                    id_produto = %(id_produto)i
            """ % {
                "preco": float(preco),
                "preco_promocao": float(preco_promocao),
                "parcelamento": int(parcelamento),
                "id_produto": int(id_produto)}

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
                    composicao = '%(composicao)s',
                    tamanho_p = %(tamanho_p)s,
                    tamanho_m = %(tamanho_m)s,
                    tamanho_g = %(tamanho_g)s
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
                "tamanho_p": tamanho_p,
                "tamanho_m": tamanho_m,
                "tamanho_g": tamanho_g,
                "id_detalhe": int(id_detalhe)}

            manipular(sql_detalhes)

            self.manipular_cores(id_produto=id_produto, cores=cores)

            manipular(sql_produto)
        else:
            # Sera feito um insert
            sql_detalhes = """
                INSERT INTO produto_detalhes(
                    descricao, id_categoria, dt_criacao,
                    id_vestuario, id_genero, url_mercado_livre,
                    url_shopee, resumo, modelo, material, composicao,
                    tamanho_p, tamanho_m, tamanho_g)
                VALUES(
                    '%s', %i, CURRENT_DATE, %i, 1, '%s', '%s', '%s',
                '%s', '%s', '%s', %s, %s, %s)
                RETURNING(id_detalhe)
                """ % (desc_produto, int(categoria), int(vestuario),
                       url_mercado_livre, url_shopee, resumo, modelo,
                       material, composicao, tamanho_p, tamanho_m, tamanho_g)

            id_detalhe = manipular(sql_detalhes, retorno=True)

            sql_produto = """
                INSERT INTO produtos VALUES(default, '%s', %i, 100)
                RETURNING(id_produto)
            """ % (produto, id_detalhe)

            id_produto = manipular(sql_produto, retorno=True)

            sql_valor = """
                INSERT INTO vendas VALUES(default, '%d', %d, %i, %i)
            """ % (float(preco), float(preco_promocao), int(parcelamento),
                   int(id_produto))

        manipular(sql_valor, retorno=False)

    def manipular_cores(self, id_produto, cores):
        """Faz a manipulacao das cores de um produto."""
        cores_old = self.buscar_produtos_cores(id_produto=id_produto)

        id_cores_old = []

        for c in cores_old:
            id_cores_old.append(int(c['id_cor']))

        sql_delete = """
            DELETE FROM
                produto_cor
            WHERE
                id_produto=%i AND id_cor=%i
        """

        for cor_old in id_cores_old:
            if cor_old not in map(int, cores):
                sql_cores = sql_delete % (int(id_produto), int(cor_old))
                manipular(sql_cores, retorno=False)

        sql_insert = """INSERT INTO produto_cor VALUES(%i, %i)"""

        for cor in cores:
            if int(cor) not in id_cores_old:
                sql_cores = sql_insert % (int(id_produto), int(cor))
                manipular(sql_cores, retorno=False)

    def excluir_produto(self, id_detalhe):
        """Faz a exclusao do produto."""
        sql_delete = """
            DELETE FROM
                produto_detalhes
            WHERE
                id_detalhe=%i
        """ % int(id_detalhe)

        manipular(sql_delete, retorno=False)

    def buscar_recomendados(
            self, id_vestuario, id_produto, id_colecao, id_categoria):
        """."""
        sql = """
            SELECT * FROM produtos p
            INNER JOIN produto_detalhes pd ON p.id_detalhe = pd.id_detalhe
            INNER JOIN vendas v ON p.id_produto = v.id_produto
            LEFT JOIN produto_imagens pi ON p.id_produto = pi.id_produto
                AND pi.destaque = True
            WHERE pd.id_vestuario = %i
            AND p.id_produto != %i
            AND (pd.id_colecao = %i OR pd.id_categoria = %i)
            LIMIT 6
        """ % (id_vestuario, id_produto, id_colecao, id_categoria)
        recomendados = consultar(sql)
        return recomendados
