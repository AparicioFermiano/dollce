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
