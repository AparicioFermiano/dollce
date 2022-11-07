from flask import Flask, render_template
from model.produtos_model import ProdutosModel

app = Flask(__name__)

produto = ProdutosModel()


@app.route("/")
def index():
    return render_template('template.html')


@app.route("/teste")
def teste():
    produtos = produto.buscar_produtos()
    return render_template('teste.html', produtos=produtos)


if __name__ == "__main__":
    app.run(debug=True)
