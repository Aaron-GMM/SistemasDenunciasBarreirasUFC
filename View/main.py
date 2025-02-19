import panel as pn
from cadastro import pagina_cadastro, botao_login
from login import pagina_login, botao_cadastro

def mostrar_cadastro(event=None):
    main_area.objects = [pagina_cadastro]

def mostrar_login(event=None):
    main_area.objects = [pagina_login]

botao_login.on_click(mostrar_login)
botao_cadastro.on_click(mostrar_cadastro)

# Criando a área principal
main_area = pn.Column(pagina_login, align="center", width=400)

# Envolvendo a área principal em uma linha para centralizar
pagina_principal = pn.Row(
    pn.layout.HSpacer(),  # Espaço à esquerda
    main_area,
    pn.layout.HSpacer(),  # Espaço à direita
    height=900
)

pn.serve(pagina_principal)
