import panel as pn
from Controller.UserController import UserController

def cadastrar_usuario(event=None):
    nome = input_nome.value
    email = input_email.value
    senha = input_senha.value

    if not nome or not email or not senha:
        mensagem.object = "❌ Todos os campos são obrigatórios!"
        return

    dados_usuario = {
        "nome": nome,
        "email": email,
        "senha": senha,
        "nivelAcesso": 2
    }

    response = UserController.insertUser(dados_usuario)

    if response["status"] == "success":
        mensagem.object = "✅ Usuário cadastrado com sucesso!"
        input_nome.value = ""
        input_email.value = ""
        input_senha.value = ""
    else:
        mensagem.object = f"❌ Erro: {response['message']}"

titulo_sistema = pn.pane.Markdown("<h1>Sistema de Denúncia de Barreiras</h1>", align="center", width=400)
logo_sistema = pn.pane.PNG("C:/Users/aaron/PycharmProjects/SistemaDenunciaUFC/View/icons/brasao4_vertical_cor_300dpi.png", width=60, height=60)
cabecalho = pn.Row( titulo_sistema,logo_sistema, align="center",  width=500)

titulo = pn.pane.Markdown("## Cadastro de Usuário", align="center")
input_nome = pn.widgets.TextInput(name="Nome")
input_email = pn.widgets.TextInput(name="E-mail")
input_senha = pn.widgets.PasswordInput(name="Senha")
botao_cadastrar = pn.widgets.Button(name="Cadastrar", button_type="primary")
botao_login = pn.widgets.Button(name="Ir para Login", button_type="light")
mensagem = pn.pane.Markdown("")

botao_cadastrar.on_click(cadastrar_usuario)

layout_cadastro = pn.Column(
    titulo,
    input_nome,
    input_email,
    input_senha,
    botao_cadastrar,
    mensagem,
    botao_login,
    align="center",
    width=400
)

pagina_cadastro = pn.Column(
    pn.Row(cabecalho, align="center"),      # Cabeçalho em uma linha centrada
    pn.Spacer(height=50),                  # Espaço vertical
    pn.Row(layout_cadastro, align="center"),  # Formulário em outra linha centrada
    align="center"
)


pagina_cadastro.servable()
