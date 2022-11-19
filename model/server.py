# -*- coding: utf-8 -*-
import psycopg2
from psycopg2.extras import RealDictCursor
import json

class Conexao(object):
    _db = None

    def __init__(self, mhost, db, usr, pwd):
        self._db = psycopg2.connect(
            host=mhost, database=db, user=usr, password=pwd
            )
        self._db.autocommit = True

    def manipular(self, sql, retorno=None):
        """Manipula os dados no db."""
        response = False
        try:
            cur = self._db.cursor()
            cur.execute(sql)
            self._db.commit()  
        except Exception:
            response = False
        if retorno:
            response = cur.fetchone()[0]
        return response

    def consultar_unit(self, sql):
        """Faz consulta com retorno unico."""
        dados = []
        try:
            cur = self._db.cursor(
               cursor_factory=RealDictCursor)
            cur.execute(sql)  
            dados = cur.fetchone() 
        except Exception as err:
            return err
        dados_dict = {k:v for k, v in dados.items()}
        return dados_dict

    def consultar(self, sql):
        """Faz a consulta no db."""
        dados = []
        try:
            cur = self._db.cursor(
               cursor_factory=RealDictCursor)
            cur.execute(sql)  
            dados = cur.fetchall() 
        except Exception as err:
            return err
        dados_dict = [{k:v for k, v in record.items()} for record in dados]
        return dados_dict

    def proximaPK(self, tabela, chave):
        """Fecha a conexao com o db."""
        sql = 'select max('+chave+') from '+tabela
        rs = self.consultar(sql)
        pk = rs[0][0]
        return pk+1

    def fechar(self):
        """Fecha a conexao com o db."""
        self._db.close()