from DAO.ORM.ormConsultas import ORMConsultas
from DAO.conexaoDAO import ConexaoDAO

class UserController:
    db = ConexaoDAO()
    conexao = db.get_conexao()
    orm = ORMConsultas(conexao)

    @staticmethod
    def _tuple_to_dict(usuario):
        if usuario:
            return {
                "id": usuario[0],
                "nome": usuario[1],
                "email": usuario[2],
                "senha": usuario[3],
                "nivelAcesso": usuario[4]
            }
        return None

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
            usuario = UserController.orm.selectById("usuario", "id", user_id)
            user_dict = UserController._tuple_to_dict(usuario)
            if user_dict:
                return {"status": "success", "data": user_dict}
            return {"status": "error", "message": "Usuário não encontrado."}
        except Exception as e:
            return {"status": "error", "message": f"Erro ao buscar usuário: {e}"}

    @staticmethod
    def getAllUsers():
        rows = UserController.orm.selectAll("usuario")
        user_list = []
        for row in rows:
            # Assume-se que a ordem das colunas seja: id, nome, email, senha, nivelAcesso
            user_list.append({
                "id": row[0],
                "nome": row[1],
                "email": row[2],
                "nivelAcesso": row[4]
            })
        return user_list

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
            usuario = UserController.orm.selectGlobal("usuario", "*", "email", email)
            if usuario:
                user = UserController._tuple_to_dict(usuario)
                if senha == user["senha"]:
                    return {"status": "success", "data": user}
                else:
                    return {"status": "error", "message": "Senha incorreta."}
            else:
                return {"status": "error", "message": "Email não encontrado."}
        except Exception as e:
            return {"status": "error", "message": f"Erro ao buscar usuário: {e}"}
