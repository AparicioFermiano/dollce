# -*- coding: utf-8 -*-
import psycopg2


class Conexao(object):
    _db = None

    def __init__(self, mhost, db, usr, pwd):
        self._db = psycopg2.connect(
            host=mhost, database=db, user=usr, password=pwd)

    def manipular(self, sql):
        """Manipula os dados no db."""
        try:
            cur = self._db.cursor()
            cur.execute(sql)
            cur.close()
            self._db.commit()
        except Exception:
            return False
        return True

    def consultar(self, sql):
        """Faz a consulta no db."""
        rs = None
        try:
            cur = self._db.cursor()
            cur.execute(sql)
            rs = cur.fetchall()
        except Exception:
            return None
        return rs

    def proximaPK(self, tabela, chave):
        """Fecha a conexao com o db."""
        sql = 'select max('+chave+') from '+tabela
        rs = self.consultar(sql)
        pk = rs[0][0]
        return pk+1

    def fechar(self):
        """Fecha a conexao com o db."""
        self._db.close()