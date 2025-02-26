import panel as pn
from Controller.UserController import UserController

def login_usuario(event=None):
    email = input_email.value.strip()
    senha = input_senha.value.strip()

    if not email or not senha:
        mensagem.object = "❌ Todos os campos são obrigatórios!"
        return

    response = UserController.loginUser(email, senha)
    if response["status"] == "success":
        user = response["data"]
        # Se for admin (nivelAcesso == 1), chama o callback passando o usuário
        if user["nivelAcesso"] == 1:
            if on_login_success:
                on_login_success(user)
        else:
            mensagem.object = "✅ Login realizado."
    else:
        mensagem.object = f"❌ {response['message']}"

# Cabeçalho: Nome do sistema e logo
titulo_sistema = pn.pane.Markdown("<h1>Sistema de Denúncia de Barreiras</h1>", align="center", width=400)
logo_sistema = pn.pane.PNG(
    r"C:\Users\aaron\PycharmProjects\SistemaDenunciaUFC\View\icons\brasao4_vertical_cor_300dpi.png",
    width=60, height=60
)
cabecalho = pn.Row(titulo_sistema, logo_sistema, align="center", width=400)

# Formulário de login
titulo_login = pn.pane.Markdown("## Login", align="center")
input_email = pn.widgets.TextInput(name="E-mail")
input_senha = pn.widgets.PasswordInput(name="Senha")
botao_entrar = pn.widgets.Button(name="Entrar", button_type="primary")
botao_cadastro = pn.widgets.Button(name="Ir para Cadastro", button_type="light")
mensagem = pn.pane.Markdown("")

botao_entrar.on_click(login_usuario)

login_form = pn.Column(
    titulo_login,
    input_email,
    input_senha,
    botao_entrar,
    botao_cadastro,
    mensagem,
    align="center",
    width=400
)

pagina_login = pn.Column(cabecalho, login_form, align="center")

# Callback que será definida externamente (no main) para tratar login bem-sucedido
on_login_success = None

__all__ = ["pagina_login", "botao_cadastro", "on_login_success"]
