import panel as pn
from Controller.localizacaoController import LocalizacaoController

atualizar_painel_callback = None

def carregar_dados_localizacao(local_id):
    response = LocalizacaoController.getLocalizacaoById(local_id)
    if response["status"] == "success":
        local = response["data"]
        input_nome.value = local["nome"]
        btn_atualizar.on_click(lambda event: atualizar_localizacao(local_id))
    else:
        mensagem.object = f"❌ {response['message']}"

def atualizar_localizacao(local_id, event=None):
    nome = input_nome.value.strip()
    if not nome:
        mensagem.object = "❌ Nome é obrigatório!"
        return
    dados = {"nome": nome}
    response = LocalizacaoController.updateLocalizacao(local_id, dados)
    if response["status"] == "success":
        mensagem.object = "✅ Localização atualizada com sucesso!"
        if atualizar_painel_callback:
            atualizar_painel_callback()
    else:
        mensagem.object = f"❌ Erro: {response['message']}"

def voltar_painel(event=None):
    import localizacaoAdm
    if localizacaoAdm.main_area:
        localizacaoAdm.main_area.objects = [localizacaoAdm.painel_localizacoes()]

titulo = pn.pane.Markdown("## Atualização de Localização", align="center")
input_nome = pn.widgets.TextInput(name="Nome")
btn_atualizar = pn.widgets.Button(name="Atualizar", button_type="primary")
btn_voltar = pn.widgets.Button(name="Voltar", button_type="warning")
btn_voltar.on_click(voltar_painel)
mensagem = pn.pane.Markdown("")

layout_update = pn.Column(
    titulo,
    input_nome,
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

__all__ = ["carregar_dados_localizacao", "pagina_update", "atualizar_painel_callback"]
