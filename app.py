from flask import Flask, render_template, abort #redirect # flash
from portal.produtos import Produtos
from datetime import date, datetime

app = Flask(__name__)
# app.config['SECRET_KEY'] = 'your secret key'

produto = Produtos()

@app.route("/")
def index_html():
    produtos = produto.buscar_produtos_card()
    return render_template(
        'portal/index.html', produtos=produtos)

@app.route("/<int:id_produto>")
def produto_html(id_produto):
    msg = ""
    if not id_produto:
        msg = "Nenhum produto encontrado!"
    dados = produto.buscar_produto_detalhes(
        id_produto=id_produto)[0]
    cores, todas_cores = produto.buscar_produtos_cores(
        id_detalhe=dados['id_detalhe'])
    imagens, imagem_destaque = produto.buscar_imagens(
        id_produto=id_produto)
    return render_template(
        'portal/produto_detalhes.html', dados=dados, 
        msg=msg, imagens=imagens, 
        imagem_destaque=imagem_destaque,
        cores=cores, todas_cores=todas_cores)

@app.route("/dollce/administracao/login")
def adm():
    produtos = produto.buscar_produto()
    return render_template(
        'gestor/gestor_produtos.html', produtos=produtos)

@app.route("/gestor/produto")
def alterar_produto():
    return render_template(
        'gestor/gestor_alterar_produto.html')

@app.errorhandler(404)
def page_not_found(e):
    return render_template('error/404.html', error=e), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('error/500.html', error=e), 500

@app.template_filter('date')
def filter_datetime(data):
    date_format = data.strftime("%d/%m/%Y")
    return date_format

if __name__ == "__main__":
    app.run(debug=True)


