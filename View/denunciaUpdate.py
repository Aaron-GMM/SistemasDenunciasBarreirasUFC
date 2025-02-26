import panel as pn
from Controller.denunciaController import DenunciaController

atualizar_painel_callback = None  # Callback configurável externamente


def carregar_dados_denuncia(denuncia_id):
    response = DenunciaController.getDenunciaById(denuncia_id)
    if response["status"] == "success":
        denuncia = response["data"]
        input_titulo.value = denuncia["titulo"]
        input_descricao.value = denuncia["descricao"]
        input_ponto_referencia.value = denuncia["ponto_referencia"]
        input_idcategoria.value = denuncia["idcategoria"]
        input_idstatus.value = denuncia["idstatus"]
        input_idusuario.value = denuncia["idusuario"]
        input_idlocalizacao.value = denuncia["idlocalizacao"]
        btn_atualizar.on_click(lambda event: atualizar_denuncia(denuncia_id))
    else:
        mensagem.object = f"❌ {response['message']}"


def atualizar_denuncia(denuncia_id, event=None):
    titulo = input_titulo.value.strip()
    descricao = input_descricao.value.strip()
    ponto_referencia = input_ponto_referencia.value.strip()
    idcategoria = input_idcategoria.value
    idstatus = input_idstatus.value
    idusuario = input_idusuario.value
    idlocalizacao = input_idlocalizacao.value

    if not titulo or not descricao:
        mensagem.object = "❌ Título e descrição são obrigatórios!"
        return

    dados = {
        "titulo": titulo,
        "descricao": descricao,
        "ponto_referencia": ponto_referencia,
        "idcategoria": idcategoria,
        "idstatus": idstatus,
        "idusuario": idusuario,
        "idlocalizacao": idlocalizacao
    }

    response = DenunciaController.updateDenuncia(denuncia_id, dados)
    if response["status"] == "success":
        mensagem.object = "✅ Denúncia atualizada com sucesso!"
        if atualizar_painel_callback:
            atualizar_painel_callback()
    else:
        mensagem.object = f"❌ Erro: {response['message']}"


def voltar_painel(event=None):
    import denunciaAdm
    if denunciaAdm.main_area:
        denunciaAdm.main_area.objects = [denunciaAdm.painel_denuncias()]


titulo_p = pn.pane.Markdown("## Atualização de Denúncia", align="center")
input_titulo = pn.widgets.TextInput(name="Título")
input_descricao = pn.widgets.TextAreaInput(name="Descrição", height=100)
input_ponto_referencia = pn.widgets.TextInput(name="Ponto de Referência")
input_idcategoria = pn.widgets.IntInput(name="ID Categoria")
input_idstatus = pn.widgets.IntInput(name="ID Status")
input_idusuario = pn.widgets.IntInput(name="ID Usuário")
input_idlocalizacao = pn.widgets.IntInput(name="ID Localização")
btn_atualizar = pn.widgets.Button(name="Atualizar", button_type="primary")
btn_voltar = pn.widgets.Button(name="Voltar", button_type="warning")
btn_voltar.on_click(voltar_painel)
mensagem = pn.pane.Markdown("")

layout_update = pn.Column(
    titulo_p,
    input_titulo,
    input_descricao,
    input_ponto_referencia,
    input_idcategoria,
    input_idstatus,
    input_idusuario,
    input_idlocalizacao,
    pn.Row(btn_atualizar, btn_voltar, align="center"),
    mensagem,
    align="center",
    width=400
)

pagina_update = pn.Column(
    pn.Spacer(height=50),
    pn.Row(layout_update, align="center"),
    align="center"
)
pagina_update.servable()

__all__ = ["carregar_dados_denuncia", "pagina_update", "atualizar_painel_callback"]
