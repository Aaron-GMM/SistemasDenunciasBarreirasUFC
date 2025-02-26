import panel as pn
from Controller.denunciaController import DenunciaController

def cadastrar_denuncia(event=None):
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

    response = DenunciaController.insertDenuncia(dados)
    if response["status"] == "success":
        mensagem.object = "✅ Denúncia cadastrada com sucesso!"
        import denunciaAdm
        if denunciaAdm.main_area:
            denunciaAdm.main_area.objects = [denunciaAdm.painel_denuncias()]
    else:
        mensagem.object = f"❌ Erro: {response['message']}"

def voltar_cadastro(event=None):
    import denunciaAdm
    if denunciaAdm.main_area:
        denunciaAdm.main_area.objects = [denunciaAdm.painel_denuncias()]

titulo = pn.pane.Markdown("## Cadastro de Denúncia", align="center")
input_titulo = pn.widgets.TextInput(name="Título")
input_descricao = pn.widgets.TextAreaInput(name="Descrição", height=100)
input_ponto_referencia = pn.widgets.TextInput(name="Ponto de Referência")
input_idcategoria = pn.widgets.IntInput(name="ID Categoria")
input_idstatus = pn.widgets.IntInput(name="ID Status")
input_idusuario = pn.widgets.IntInput(name="ID Usuário")
input_idlocalizacao = pn.widgets.IntInput(name="ID Localização")
btn_cadastrar = pn.widgets.Button(name="Cadastrar", button_type="primary")
btn_voltar = pn.widgets.Button(name="Voltar", button_type="warning")
btn_cadastrar.on_click(cadastrar_denuncia)
btn_voltar.on_click(voltar_cadastro)
mensagem = pn.pane.Markdown("")

layout_cadastro = pn.Column(
    titulo,
    input_titulo,
    input_descricao,
    input_ponto_referencia,
    input_idcategoria,
    input_idstatus,
    input_idusuario,
    input_idlocalizacao,
    pn.Row(btn_cadastrar, btn_voltar, align="center"),
    mensagem,
    align="center",
    width=400
)

pagina_cadastrar = pn.Column(
    pn.Spacer(height=50),
    pn.Row(layout_cadastro, align="center"),
    align="center"
)
pagina_cadastrar.servable()

def pagina_cadastrar_denuncia():
    return pagina_cadastrar

__all__ = ["pagina_cadastrar_denuncia"]
