# -*- coding: utf-8 -*-
from model.produtos_model import ProdutosModel


class Produtos():
    """Gerenciamento de produtos."""

    def __init__(self):
        """Construtor."""
        self.produtos_model = ProdutosModel()

    def fabrica_produto(self):
        """."""
        produtos = self.produtos_model.buscar_produtos()
        return produtos


