import panel as pn
from Controller.UserController import UserController


def login_usuario(event=None):
    email = input_email_login.value
    senha = input_senha_login.value

    if not email or not senha:
        mensagem.object = "❌ Todos os campos são obrigatórios!"
        return

    response = UserController.loginUser(email, senha)

    if response["status"] == "success":
        mensagem.object = "✅ Login realizado com sucesso!"
    else:
        mensagem.object = f"❌ {response['message']}"
# Criando o cabeçalho fixo no topo
titulo_sistema = pn.pane.Markdown("<h1>Sistema de Denúncia de Barreiras</h1>", align="center", width=400)
logo_sistema = pn.pane.PNG("C:/Users/aaron/PycharmProjects/SistemaDenunciaUFC/View/icons/brasao4_vertical_cor_300dpi.png", width=60, height=60)
cabecalho = pn.Row( titulo_sistema,logo_sistema, align="center",  width=400)

# Criando os componentes do painel
titulo_login = pn.pane.Markdown("## Login", align="center")
input_email_login = pn.widgets.TextInput(name="E-mail")
input_senha_login = pn.widgets.PasswordInput(name="Senha")
botao_entrar = pn.widgets.Button(name="Entrar", button_type="primary")
botao_cadastro = pn.widgets.Button(name="Ir para Cadastro", button_type="light")
mensagem = pn.pane.Markdown("")

botao_entrar.on_click(login_usuario)

inputs = pn.Column(
input_email_login,
    input_senha_login,
    align="center",
    width=400
)

# Layout da página de login
layout_login = pn.Column(

    titulo_login,
    inputs,
    botao_entrar,
    botao_cadastro,
    mensagem,
    align="center",
    width=400
)

# Criando a estrutura completa da página
pagina_login = pn.Column(
    cabecalho,  # Espaço para afastar o cabeçalho do formulário
    pn.Row(layout_login, align="center"),

)

pagina_login.servable()
