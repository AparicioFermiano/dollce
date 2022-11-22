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
        imagens = self.produtos_model.buscar_imagens(
            id_produto=id_produto)
        imagem_destaque = None

        for i in imagens:
            if i['destaque']:
                imagem_destaque = i

        return imagens, imagem_destaque

    def gerar_card_produto(self):
        """Gera o card do produto."""
        produto = self.produtos_model.buscar_produtos_card()
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

        self.produtos_model.manipular_produto(
            id_produto=form.get('id_produto', None),
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
            cores=cores)

    def excluir_produto(self, id_detalhe):
        """Excluir o produto."""
        self.produtos_model.excluir_produto(
            id_detalhe=id_detalhe)

    def buscar_recomendados(
            self, id_produto, id_categoria, id_colecao,
            id_vestuario):
        """Faz a busca de itens recomendados."""
        return self.produtos_model.buscar_recomendados(
            id_produto=id_produto, id_vestuario=id_vestuario,
            id_colecao=id_colecao, id_categoria=id_categoria
        )
