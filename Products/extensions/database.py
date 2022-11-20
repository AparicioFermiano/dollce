"""Database."""
import psycopg2
from psycopg2.extras import RealDictCursor


db = psycopg2.connect(
    host='localhost', database='dollce', user='aparicio',
    password='@Aparicio129')

db.autocommit = True


def manipular(sql, retorno=None):
    """Manipula os dados no db."""
    response = False
    try:
        cur = db.cursor()
        cur.execute(sql)
        db.commit()
    except Exception as err:
        raise Exception('Erro no banco!, %s' % err)
    if retorno:
        response = cur.fetchone()[0]
    return response


def consultar_unit(sql):
    """Faz consulta com retorno unico."""
    dados = []
    try:
        cur = db.cursor(cursor_factory=RealDictCursor)
        cur.execute(sql)
        dados = cur.fetchone()
    except Exception as err:
        return err
    if dados:
        dados = {k: v for k, v in dados.items()}
    return dados


def consultar(sql):
    """Faz a consulta no db."""
    dados = []
    try:
        cur = db.cursor(cursor_factory=RealDictCursor)
        cur.execute(sql)
        dados = cur.fetchall()
    except Exception as err:
        return err
    dados_dict = [{k: v for k, v in record.items()} for record in dados]
    return dados_dict


def fechar():
    """Fecha a conexao com o db."""
    db.close()


def init_app(app):
    """."""
    db.init_app(app)
