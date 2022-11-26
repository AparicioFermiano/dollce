#!/usr/bin/env python
# -*- coding: utf-8 -*-

from Products.portal.produtos import Produtos
from flask import render_template, request, flash
from flask import redirect, url_for, session

produto = Produtos()


def init_app(app):
    """Inicializa a extensao."""
    @app.route("/")
    def index_html():
        """."""
        produtos = produto.gerar_card_produto()
        return render_template(
            'portal/index.html', produtos=produtos)

    @app.route("/produto/<int:id_produto>")
    def produto_html(id_produto):
        """."""
        dados = produto.buscar_produto_detalhes(
            id_produto=id_produto)
        if not dados:
            flash('Produto não encontrado!', 'alert-warning')
            return redirect(url_for('index_html'))
        recomendados = produto.buscar_recomendados(
            id_produto=dados['id_produto'],
            id_vestuario=dados['id_vestuario'],
            id_colecao=dados['id_colecao'],
            id_categoria=dados['id_categoria'])
        cores, todas_cores = produto.verificar_cores_produtos(
            id_produto=dados['id_produto'], todas_cores=True)
        imagens = produto.buscar_imagens_produto(
            id_produto=id_produto)
        return render_template(
            'portal/produto_detalhes.html', dados=dados,
            imagens=imagens, cores=cores, todas_cores=todas_cores,
            recomendados=recomendados)

    @app.route("/dollce/administracao/home", methods=['GET', 'POST'])
    def adm():
        """."""
        produtos = produto.buscar_produtos()

        if request.method == 'POST':
            id_detalhe = request.form.get('id_detalhe', None)
            if id_detalhe:
                try:
                    produto.excluir_produto(id_detalhe=id_detalhe)
                    msg = 'Produto excluído com sucesso.'
                    alert = 'alert-success'
                except Exception as err:
                    msg = 'Erro na exclusão: %s' % err
                    alert = 'alert-danger'
                flash(msg, alert)
                return redirect(url_for('adm'))

        return render_template(
            'gestor/gestor_produtos.html', produtos=produtos)

    @app.route("/dollce/administracao/produto", methods=['GET', 'POST'])
    def alterar_produto():
        """."""
        session.pop('_flashes', None)
        lista_cores = produto.listar_cores()
        lista_vestuario = produto.listar_vestuario()
        id_produto = request.args.get('id_produto', None)
        id_vestuario = request.args.get('id_vestuario', None)
        detalhes = []
        cores = []

        if id_produto:
            detalhes = produto.buscar_produto_detalhes(
                id_produto=int(id_produto))
            if not detalhes:
                flash('Produto não localizado', 'alert-danger')
                return redirect(url_for('adm'))
            for cor in produto.verificar_cores_produtos(
                    id_produto=int(id_produto)):
                cores.append(cor['id_cor'])
            imagens = produto.buscar_imagens_produto(
                id_produto=int(id_produto))
        if id_vestuario:
            lista_categoria = produto.listar_categorias(
                id_vestuario=id_vestuario)
            return lista_categoria

        if request.method == 'POST':
            try:
                produto.manipular_produto(form=request.form)
                msg = 'Cadastro realizado com sucesso.'
                alert = 'alert-success'
            except Exception as e:
                msg = 'Erro: %s' % e
                alert = 'alert-danger'
            flash(msg, alert)
            return redirect(url_for('adm'))
        return render_template(
            'gestor/gestor_alterar_produto.html',
            detalhes=detalhes,
            lista_cores=lista_cores,
            lista_vestuario=lista_vestuario,
            cores=cores, imagens=imagens)

    @app.route("/teste", methods=['GET', 'POST'])
    def teste():
        """teste."""
        if request.method == 'POST':
            flash('Erro na alteração. Tente novamente!', 'alert-danger')
        # session['_flashes'].clear()

        return render_template('teste.html')

    # @app.errorhandler(404)
    # def page_not_found(e):
    #     return render_template('error/404.html', error=e), 404

    # @app.errorhandler(500)
    # def internal_server_error(e):
    #     return render_template('error/500.html', error=e), 500

    @app.template_filter('date')
    def filter_datetime(data):
        """Filtro."""
        date_format = data.strftime("%d/%m/%Y")
        return date_format
