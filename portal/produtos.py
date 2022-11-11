# -*- coding: utf-8 -*-
from model.produtos_model import ProdutosModel


class Produtos():
    """Gerenciamento de produtos."""

    def __init__(self):
        """Construtor."""
        self.produtos_model = ProdutosModel()

    def buscar_produto(self, id_produto=None):
        """Busca os produtos """
        produtos = self.produtos_model.buscar_produtos(
            id_produto=id_produto)
        return produtos

    def buscar_imagens(self, id_produto=None):
        """."""
        imagens = self.produtos_model.buscar_imagens(
            id_produto=id_produto)
        imagem_destaque = None
        for i in imagens:
            if i['destaque']:
                imagem_destaque = i
        return imagens, imagem_destaque
