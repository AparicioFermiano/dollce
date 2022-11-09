from flask import Flask, render_template, redirect # flash
from portal.produtos import Produtos

app = Flask(__name__)
# app.config['SECRET_KEY'] = 'your secret key'

produto = Produtos()

@app.route("/")
def index_html():
    produtos = produto.buscar_produto()
    return render_template(
        'index.html', produtos=produtos)

@app.route("/produto/<int:id_produto>")
def produto_html(id_produto):
    msg = ""
    if not id_produto:
        msg = "Nenhum produto encontrado!"
    dados = produto.buscar_produto(
        id_produto=id_produto)
    return render_template(
        'produto.html', dados=dados, msg=msg)

if __name__ == "__main__":
    app.run(debug=True)


