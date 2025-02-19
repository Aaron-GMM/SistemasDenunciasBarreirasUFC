import psycopg2

class ConexaoDAO:
    def __init__(self):
        self.conexao = psycopg2.connect(
            database="SDBDUFC",
            host="localhost",
            user="postgres",
            password="root",
            port="5432"
        )

    def get_conexao(self):
        return self.conexao

    def close_conexao(self):
        if self.conexao:
            self.conexao.close()
