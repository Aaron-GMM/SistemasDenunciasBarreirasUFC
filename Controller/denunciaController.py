from DAO.ORM.ormConsultas import ORMConsultas
from DAO.conexaoDAO import ConexaoDAO

class DenunciaController:
    db = ConexaoDAO()
    conexao = db.get_conexao()
    orm = ORMConsultas(conexao)

    @staticmethod
    def _tuple_to_dict(denuncia):
        if denuncia:
            return {
                "id": denuncia[0],
                "descricao": denuncia[1],
                "titulo": denuncia[2],
                "ponto_referencia": denuncia[3],
                "idcategoria": denuncia[4],
                "idstatus": denuncia[5],
                "idusuario": denuncia[6],
                "idlocalizacao": denuncia[7]
            }
        return None

    @staticmethod
    def insertDenuncia(dados):
        try:
            DenunciaController.orm.insert("denuncia", dados)
            return {"status": "success", "message": "Denúncia inserida com sucesso.", "data": dados}
        except Exception as e:
            return {"status": "error", "message": f"Erro ao inserir denúncia: {e}"}

    @staticmethod
    def getDenunciaById(denuncia_id):
        try:
            denuncia = DenunciaController.orm.selectById("denuncia", "id", denuncia_id)
            denuncia_dict = DenunciaController._tuple_to_dict(denuncia)
            if denuncia_dict:
                return {"status": "success", "data": denuncia_dict}
            return {"status": "error", "message": "Denúncia não encontrada."}
        except Exception as e:
            return {"status": "error", "message": f"Erro ao buscar denúncia: {e}"}

    @staticmethod
    def getAllDenuncias():
        rows = DenunciaController.orm.selectAll("denuncia")
        denuncia_list = []
        for row in rows:
            denuncia_list.append({
                "id": row[0],
                "descricao": row[1],
                "titulo": row[2],
                "ponto_referencia": row[3],
                "idcategoria": row[4],
                "idstatus": row[5],
                "idusuario": row[6],
                "idlocalizacao": row[7]
            })
        return denuncia_list

    @staticmethod
    def updateDenuncia(denuncia_id, dados):
        try:
            DenunciaController.orm.UpdateById("denuncia", "id", denuncia_id, dados)
            return {"status": "success", "message": "Denúncia atualizada com sucesso.", "data": dados}
        except Exception as e:
            return {"status": "error", "message": f"Erro ao atualizar denúncia: {e}"}

    @staticmethod
    def deleteDenuncia(denuncia_id):
        try:
            DenunciaController.orm.deleteById("denuncia", "id", denuncia_id)
            return {"status": "success", "message": "Denúncia deletada com sucesso.", "id": denuncia_id}
        except Exception as e:
            return {"status": "error", "message": f"Erro ao deletar denúncia: {e}"}
