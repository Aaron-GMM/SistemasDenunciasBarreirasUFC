import panel as pn
from cadastro import pagina_cadastro, botao_login  # Caso você possua a tela de cadastro
from login import pagina_login, botao_cadastro as btn_ir_para_cadastro
import login
import userAdm
from userAdm import set_main_area as set_user_main
from denunciaAdm import set_main_area as set_denuncia_main
from localizacaoAdm import set_main_area as set_localizacao_main


# Área principal que exibe as telas (inicia com a tela de login)
main_area = pn.Column(pagina_login, align="center", width=400)

set_user_main(main_area)
set_denuncia_main(main_area)
set_localizacao_main(main_area)

# Define o main_area no módulo de administração para permitir a atualização do painel
userAdm.set_main_area(main_area)

def mostrar_cadastro(event=None):
    main_area.objects = [pagina_cadastro]

def mostrar_login(event=None):
    main_area.objects = [pagina_login]

botao_login.on_click(mostrar_login)
btn_ir_para_cadastro.on_click(mostrar_cadastro)

def handle_login_success(user):
    # Se o usuário for admin (nivelAcesso == 1), exibe o painel de usuários;
    # caso contrário, exibe uma mensagem de boas-vindas.
    if user["nivelAcesso"] == 1:
        main_area.objects = [userAdm.painel_usuarios()]
    else:
        main_area.objects = [pn.pane.Markdown(f"Bem-vindo, {user['nome']}!")]

# Atribui o callback de sucesso de login no módulo de login
login.on_login_success = handle_login_success

# Layout final centralizado
pagina_principal = pn.Row(
    pn.layout.HSpacer(),
    main_area,
    pn.layout.HSpacer(),
    height=900
)

pn.serve(pagina_principal)
