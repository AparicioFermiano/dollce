from flask import Flask, render_template
from portal.produtos import Produtos

app = Flask(__name__)

produto = Produtos()


@app.route("/")
def index():
    produtos = produto.fabrica_produto()
    return render_template(
        'template.html', produtos=produtos)

if __name__ == "__main__":
    app.run(debug=True)
