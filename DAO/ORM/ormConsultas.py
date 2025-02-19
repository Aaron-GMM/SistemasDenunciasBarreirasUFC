class ORMConsultas:
    def __init__(self, conexao):
        self.conexao = conexao

    def insert(self, tabela, dados):
        colunas = ', '.join(dados.keys())
        valores = ', '.join(['%s'] * len(dados))
        sql = f"INSERT INTO {tabela} ({colunas}) VALUES ({valores})"
        try:
            with self.conexao.cursor() as cursor:
                cursor.execute(sql, tuple(dados.values()))
                self.conexao.commit()
                print(f"[DEBUG] Insert realizado com sucesso em '{tabela}'. Dados: {dados}")
        except Exception as e:
            print(f"[DEBUG] Erro no INSERT em '{tabela}': {e}")

    def selectById(self, tabela, id_coluna, id_valor):
        sql = f"SELECT * FROM {tabela} WHERE {id_coluna} = %s"
        try:
            with self.conexao.cursor() as cursor:
                cursor.execute(sql, (id_valor,))
                resultado = cursor.fetchone()
                print(f"[DEBUG] Select por ID em '{tabela}'. Resultado: {resultado}")
                return resultado
        except Exception as e:
            print(f"[DEBUG] Erro no SELECT em '{tabela}': {e}")

    def selectGlobal(self, tabela, coluna, campo, valor):
        sql = f"SELECT {coluna} FROM {tabela} WHERE {campo} = %s"
        try:
            with self.conexao.cursor() as cursor:
                cursor.execute(sql,(valor,))
                resultado = cursor.fetchone()
                print(f"[DEBUG] Select por ID em '{tabela}'. Resultado: {resultado}")
                return resultado
        except Exception as e:
                print(f"[DEBUG] Erro no SELECT em '{tabela}': {e}")

    def deleteById(self, tabela, id_coluna, id_valor):
        sql = f"DELETE FROM {tabela} WHERE {id_coluna} = %s"
        try:
            with self.conexao.cursor() as cursor:
                cursor.execute(sql, (id_valor,))
                self.conexao.commit()
                print(f"[DEBUG] Delete realizado com sucesso em '{tabela}', ID: {id_valor}")
        except Exception as e:
            print(f"[DEBUG] Erro no DELETE em '{tabela}': {e}")

    def UpdateById(self, tabela, id_coluna, id_valor, dados):

        colunas = ', '.join([f"{k} = %s" for k in dados.keys()])
        sql = f"UPDATE {tabela} SET {colunas} WHERE {id_coluna} = %s"
        try:
            with self.conexao.cursor() as cursor:
                cursor.execute(sql, tuple(dados.values()) + (id_valor,))
                self.conexao.commit()
                print(f"[DEBUG] Update realizado com sucesso em '{tabela}'. ID: {id_valor}, Dados: {dados}")
        except Exception as e:
            print(f"[DEBUG] Erro no UPDATE em '{tabela}': {e}")
