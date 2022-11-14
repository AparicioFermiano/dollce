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

    def buscar_produtos_cores(self, id_detalhe):
        """Busca os detalhes do produto."""
        cores = self.produtos_model.buscar_produtos_cores(
            id_detalhe=id_detalhe)
        todas_cores = []

        for cor in cores:
            todas_cores.append(cor['cor'])

        todas_cores = str(todas_cores).strip('[]').replace("'", '')
        
        return cores, todas_cores

    def buscar_imagens(self, id_produto=None):
        """."""
        imagens = self.produtos_model.buscar_imagens(
            id_produto=id_produto)
        imagem_destaque = None
        
        for i in imagens:
            if i['destaque']:
                imagem_destaque = i
        
        return imagens, imagem_destaque
