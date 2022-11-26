"""Controller de produtos."""
from Products.model.produtos_model import ProdutosModel


class Produtos():
    """Gerenciamento de produtos."""

    def __init__(self):
        """Construtor."""
        self.produtos_model = ProdutosModel()

    def buscar_produtos(self):
        """Busca os produtos."""
        produtos = self.produtos_model.buscar_produtos()

        return produtos

    def buscar_produto_detalhes(self, id_produto):
        """Busca os detalhes do produto."""
        detalhes = self.produtos_model.buscar_produto_detalhes(
            id_produto=id_produto)
        detalhes['preco_parcelado'] = detalhes[
            'preco_promocao'] / detalhes['parcelamento']
        if not detalhes['id_colecao']:
            detalhes['id_colecao'] = 1
        return detalhes

    def verificar_cores_produtos(self, id_produto, todas_cores=False):
        """Verifica as cores disponiveis do produto."""
        cores = self.produtos_model.buscar_produtos_cores(
            id_produto=id_produto)

        if todas_cores:
            todas_cores = []

            for cor in cores:
                todas_cores.append(cor['cor'])

            todas_cores = str(todas_cores).strip('[]').replace("'", '')

            return cores, todas_cores

        return cores

    def buscar_imagens_produto(self, id_produto=None):
        """Busca todas imagens relacionada a um produto."""
        imagem = {}

        for i in self.produtos_model.buscar_imagens(
                id_produto=id_produto):
            if i['ordem'] == 1:
                imagem['imagem_destaque'] = i['url_imagem']
            elif i['ordem'] == 2:
                imagem['imagem_secundaria'] = i['url_imagem']
            elif i['ordem'] == 3:
                imagem['imagem_adicional1'] = i['url_imagem']
            else:
                imagem['imagem_adicional2'] = i['url_imagem']

        return imagem

    def gerar_card_produto(self):
        """Gera o card do produto."""
        produto = self.produtos_model.buscar_produtos_card()
        for p in produto:
            preco_parcelado = float(
                p['preco_promocao']) / int(p['parcelamento'])
            p['preco_parcelado'] = round(preco_parcelado, 2)
            if not p['imagem_principal']:
                p['imagem_principal'] = 'image/modelo.jfif'
            if not p['imagem_secundaria']:
                p['imagem_secundaria'] = 'image/modelo1.jfif'
        return produto

    def listar_cores(self):
        """Gera a lista das cores."""
        cores = self.produtos_model.buscar_cores()
        return cores

    def listar_categorias(self, id_vestuario):
        """Gera a lista de categorias."""
        categorias = self.produtos_model.buscar_categorias(
            id_vestuario=id_vestuario)
        return categorias

    def listar_vestuario(self):
        """Gera a lista de categorias."""
        vestuario = self.produtos_model.buscar_vestuario()
        return vestuario

    def manipular_produto(self, form=None):
        """Valida os dados e manipula o produto."""
        cores = []
        for item in form:
            if 'cor' in item:
                cores.append(form.get(item))

        id_produto = form.get('id_produto', None)

        self.produtos_model.manipular_imagem(
            id_produto=id_produto,
            imagem_principal=form.get('imagem_principal', None),
            imagem_secundaria=form.get('imagem_secundaria', None),
            imagem_adicional1=form.get('imagem_adicional1', None),
            imagem_adicional2=form.get('imagem_adicional2', None))

        return self.produtos_model.manipular_produto(
            id_produto=id_produto,
            id_detalhe=form.get('id_detalhe', None),
            produto=form.get('produto', None),
            desc_produto=form.get('desc_produto', None),
            vestuario=form.get('vestuario', None),
            categoria=form.get('categoria', None),
            resumo=form.get('resumo', None),
            url_mercado_livre=form.get('url_mercado_livre', None),
            url_shopee=form.get('url_shopee', None),
            modelo=form.get('modelo', None),
            material=form.get('material', None),
            composicao=form.get('composicao', None),
            tamanho_p=form.get('tamanho_p', False),
            tamanho_m=form.get('tamanho_m', False),
            tamanho_g=form.get('tamanho_g', False),
            preco=form.get('preco', None),
            preco_promocao=form.get('preco_promocao', None),
            parcelamento=form.get('parcelamento', None),
            cores=cores)

    # def manipular_imagem(self, form=None)

    def excluir_produto(self, id_detalhe):
        """Excluir o produto."""
        self.produtos_model.excluir_produto(
            id_detalhe=id_detalhe)

    def buscar_recomendados(
            self, id_produto, id_categoria, id_vestuario, id_colecao):
        """Faz a busca de itens recomendados."""
        recomendados = self.produtos_model.buscar_recomendados(
            id_produto=int(id_produto), id_vestuario=int(id_vestuario),
            id_colecao=int(id_colecao), id_categoria=int(id_categoria)
        )

        if recomendados:
            for r in recomendados:
                r['preco_parcelado'] = r['preco_promocao'] / r['parcelamento']
        else:
            recomendados = []

        return recomendados
