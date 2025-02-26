import panel as pn
from Controller.localizacaoController import LocalizacaoController

def cadastrar_localizacao(event=None):
    nome = input_nome.value.strip()
    if not nome:
        mensagem.object = "❌ Nome é obrigatório!"
        return
    dados = {"nome": nome}
    response = LocalizacaoController.insertLocalizacao(dados)
    if response["status"] == "success":
        mensagem.object = "✅ Localização cadastrada com sucesso!"
        import localizacaoAdm
        if localizacaoAdm.main_area:
            localizacaoAdm.main_area.objects = [localizacaoAdm.painel_localizacoes()]
    else:
        mensagem.object = f"❌ Erro: {response['message']}"

def voltar_cadastro(event=None):
    import localizacaoAdm
    if localizacaoAdm.main_area:
        localizacaoAdm.main_area.objects = [localizacaoAdm.painel_localizacoes()]

titulo = pn.pane.Markdown("## Cadastro de Localização", align="center")
input_nome = pn.widgets.TextInput(name="Nome")
btn_cadastrar = pn.widgets.Button(name="Cadastrar", button_type="primary")
btn_voltar = pn.widgets.Button(name="Voltar", button_type="warning")
btn_cadastrar.on_click(cadastrar_localizacao)
btn_voltar.on_click(voltar_cadastro)
mensagem = pn.pane.Markdown("")

layout_cadastro = pn.Column(
    titulo,
    input_nome,
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

def pagina_cadastrar_localizacao():
    return pagina_cadastrar

__all__ = ["pagina_cadastrar_localizacao"]
