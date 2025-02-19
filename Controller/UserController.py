from DAO.ORM.ormConsultas import ORMConsultas
from DAO.conexaoDAO import ConexaoDAO


class UserController:

    db = ConexaoDAO()
    conexao = db.get_conexao()
    orm = ORMConsultas(conexao)

    @staticmethod
    def insertUser(dados):
        try:
            UserController.orm.insert("usuario", dados)
            return {"status": "success", "message": "Usuário inserido com sucesso.", "data": dados}
        except Exception as e:
            return {"status": "error", "message": f"Erro ao inserir usuário: {e}"}

    @staticmethod
    def getUserById(user_id):
        try:
            user = UserController.orm.selectById("usuario", "id", user_id)
            if user:
                return {"status": "success", "data": user}
            return {"status": "error", "message": "Usuário não encontrado."}
        except Exception as e:
            return {"status": "error", "message": f"Erro ao buscar usuário: {e}"}

    @staticmethod
    def updateUser(user_id, dados):

        try:
            UserController.orm.UpdateById("usuario", "id", user_id, dados)
            return {"status": "success", "message": "Usuário atualizado com sucesso.", "data": dados}
        except Exception as e:
            return {"status": "error", "message": f"Erro ao atualizar usuário: {e}"}

    @staticmethod
    def deleteUser(user_id):

        try:
            UserController.orm.deleteById("usuario", "id", user_id)
            return {"status": "success", "message": "Usuário deletado com sucesso.", "user_id": user_id}
        except Exception as e:
            return {"status": "error", "message": f"Erro ao deletar usuário: {e}"}

    @staticmethod
    def loginUser(email, senha):
        try:
            # Buscar o usuário pelo e-mail
            usuario = UserController.orm.selectGlobal("usuario", "*", "email", email)

            if usuario:
                senha_banco = usuario[3]  # Supondo que a senha está na terceira coluna

                if senha == senha_banco:
                    return {"status": "success", "data": usuario}
                else:
                    return {"status": "error", "message": "Senha incorreta."}
            else:
                return {"status": "error", "message": "Email não encontrado."}

        except Exception as e:
            return {"status": "error", "message": f"Erro ao buscar usuário: {e}"}

