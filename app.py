from flask import Flask, render_template, abort, request, jsonify #redirect flash
from portal.produtos import Produtos
from datetime import date, datetime
from time import time

app = Flask(__name__)
# app.config['SECRET_KEY'] = 'your secret key'

produto = Produtos()

@app.route("/")
def index_html():
    produtos = produto.gerar_card_produto()
    return render_template(
        'portal/index.html', produtos=produtos)

@app.route("/<int:id_produto>")
def produto_html(id_produto):
    if not id_produto:
        raise Exception("Nenhum produto encontrado!")
    dados = produto.buscar_produto_detalhes(
        id_produto=id_produto)[0]
    cores, todas_cores = produto.verificar_cores_produtos(
        id_detalhe=dados['id_detalhe'])
    imagens, imagem_destaque = produto.buscar_imagens_produto(
        id_produto=id_produto)
    return render_template(
        'portal/produto_detalhes.html', dados=dados, 
        imagens=imagens, 
        imagem_destaque=imagem_destaque,
        cores=cores, todas_cores=todas_cores)

@app.route("/dollce/administracao/login")
def adm():
    produtos = produto.buscar_produto()
    return render_template(
        'gestor/gestor_produtos.html', produtos=produtos)

@app.route("/dollce/administracao/produto", methods=['GET', 'POST'])
def alterar_produto():
    lista_cores = produto.listar_cores()
    lista_vestuario = produto.listar_vestuario()
    id_produto = request.args.get('id_produto', None)
    id_vestuario = request.args.get('id_vestuario', None)
    detalhes = []
    cores = []
    tamanhos = []

    if id_produto:
        detalhes = produto.buscar_produto_detalhes(
            id_produto=int(id_produto))
        # cores = produto.buscar_produto_detalhes(
        #     id_produto=int(id_produto))
    if id_vestuario:
        lista_categoria = produto.listar_categorias(
            id_vestuario=id_vestuario)
        return lista_categoria
    if request.method == 'POST':
        produto.manipular_produto(form=request.form)

    return render_template(
        'gestor/gestor_alterar_produto.html', 
        detalhes=detalhes,
        lista_cores=lista_cores, 
        lista_vestuario=lista_vestuario)

# @app.errorhandler(404)
# def page_not_found(e):
#     return render_template('error/404.html', error=e), 404

# @app.errorhandler(500)
# def internal_server_error(e):
#     return render_template('error/500.html', error=e), 500

@app.template_filter('date')
def filter_datetime(data):
    date_format = data.strftime("%d/%m/%Y")
    return date_format

if __name__ == "__main__":
    app.run(debug=True)


