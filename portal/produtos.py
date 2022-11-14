# -*- coding: utf-8 -*-
from model.produtos_model import ProdutosModel


class Produtos():
    """Gerenciamento de produtos."""

    def __init__(self):
        """Construtor."""
        self.produtos_model = ProdutosModel()

    def buscar_produto(self):
        """Busca os produtos."""
        produtos = self.produtos_model.buscar_produtos()
        
        return produtos

    def buscar_produto_detalhes(self, id_produto):
        """Busca os detalhes do produto."""
        if not id_produto:
            raise Exception("É necessário o id do produto")
        
        detalhes = self.produtos_model.buscar_produto_detalhes(
            id_produto=id_produto)
        
        return detalhes

    def verificar_cores_produtos(self, id_detalhe):
        """Verifica as cores disponiveis do produto."""
        cores = self.produtos_model.buscar_produtos_cores(
            id_detalhe=id_detalhe)
        todas_cores = []

        for cor in cores:
            todas_cores.append(cor['cor'])

        todas_cores = str(todas_cores).strip('[]').replace("'", '')
        
        return cores, todas_cores

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
