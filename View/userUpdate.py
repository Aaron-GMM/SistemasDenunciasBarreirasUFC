import panel as pn
from Controller.UserController import UserController

atualizar_painel_callback = None  # Callback configurável externamente

def carregar_dados_usuario(user_id):
    response = UserController.getUserById(user_id)
    if response["status"] == "success":
        usuario = response["data"]
        input_nome.value = usuario["nome"]
        input_email.value = usuario["email"]
        input_senha.value = usuario["senha"]  # Não preenche a senha por segurança
        input_Na.value = usuario["nivelAcesso"]
        botao_atualizar.on_click(lambda event: atualizar_usuario(user_id))
    else:
        mensagem.object = f"❌ {response['message']}"

def atualizar_usuario(user_id, event=None):
    nome = input_nome.value.strip()
    email = input_email.value.strip()
    senha = input_senha.value.strip()
    # Removido o .strip() pois input_Na.value já é um int
    nivelAcesso = input_Na.value
    if not nome or not email:
        mensagem.object = "❌ Nome e e-mail são obrigatórios!"
        return

    dados_usuario = {
        "nome": nome,
        "email": email,
        "senha": senha,
        "nivelAcesso": nivelAcesso
    }

    response = UserController.updateUser(user_id, dados_usuario)
    if response["status"] == "success":
        mensagem.object = "✅ Usuário atualizado com sucesso!"
        if atualizar_painel_callback:
            atualizar_painel_callback()
    else:
        mensagem.object = f"❌ Erro: {response['message']}"

def voltar_painel(event=None):
    import userAdm
    if userAdm.main_area:
        userAdm.main_area.objects = [userAdm.painel_usuarios()]

# Elementos da tela de atualização
titulo = pn.pane.Markdown("## Atualização de Usuário", align="center")
input_nome = pn.widgets.TextInput(name="Nome")
input_email = pn.widgets.TextInput(name="E-mail")
input_senha = pn.widgets.PasswordInput(name="Senha")
input_Na = pn.widgets.IntInput(name="Nível de Acesso")
botao_atualizar = pn.widgets.Button(name="Atualizar", button_type="primary")
botao_voltar = pn.widgets.Button(name="Voltar", button_type="warning")
botao_voltar.on_click(voltar_painel)
mensagem = pn.pane.Markdown("")

layout_update = pn.Column(
    titulo,
    input_nome,
    input_email,
    input_senha,
    input_Na,
    pn.Row(botao_atualizar, botao_voltar, align="center"),
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

__all__ = ["carregar_dados_usuario", "pagina_update", "atualizar_painel_callback"]
