from DAO.ORM.ormConsultas import ORMConsultas
from DAO.conexaoDAO import ConexaoDAO

class LocalizacaoController:
    db = ConexaoDAO()
    conexao = db.get_conexao()
    orm = ORMConsultas(conexao)

    @staticmethod
    def _tuple_to_dict(localizacao):
        if localizacao:
            return {
                "id": localizacao[0],
                "nome": localizacao[1]
            }
        return None

    @staticmethod
    def insertLocalizacao(dados):
        try:
            LocalizacaoController.orm.insert("localizacao", dados)
            return {"status": "success", "message": "Localização inserida com sucesso.", "data": dados}
        except Exception as e:
            return {"status": "error", "message": f"Erro ao inserir localização: {e}"}

    @staticmethod
    def getLocalizacaoById(localizacao_id):
        try:
            localizacao = LocalizacaoController.orm.selectById("localizacao", "id", localizacao_id)
            localizacao_dict = LocalizacaoController._tuple_to_dict(localizacao)
            if localizacao_dict:
                return {"status": "success", "data": localizacao_dict}
            return {"status": "error", "message": "Localização não encontrada."}
        except Exception as e:
            return {"status": "error", "message": f"Erro ao buscar localização: {e}"}

    @staticmethod
    def getAllLocalizacoes():
        rows = LocalizacaoController.orm.selectAll("localizacao")
        local_list = []
        for row in rows:
            local_list.append({
                "id": row[0],
                "nome": row[1]
            })
        return local_list

    @staticmethod
    def updateLocalizacao(localizacao_id, dados):
        try:
            LocalizacaoController.orm.UpdateById("localizacao", "id", localizacao_id, dados)
            return {"status": "success", "message": "Localização atualizada com sucesso.", "data": dados}
        except Exception as e:
            return {"status": "error", "message": f"Erro ao atualizar localização: {e}"}

    @staticmethod
    def deleteLocalizacao(localizacao_id):
        try:
            LocalizacaoController.orm.deleteById("localizacao", "id", localizacao_id)
            return {"status": "success", "message": "Localização deletada com sucesso.", "id": localizacao_id}
        except Exception as e:
            return {"status": "error", "message": f"Erro ao deletar localização: {e}"}
