import panel as pn
import pandas as pd
from Controller.UserController import UserController
from userUpdate import carregar_dados_usuario, pagina_update

main_area = None  # Será definido via set_main_area
atualizar_painel_callback = None

# Widgets para filtro e ordenação
filtro_nivel = pn.widgets.Select(
    name="Filtrar por Nível",
    options={"Todos": "todos", "Nível 1": 1, "Nível 2": 2},
    value="todos"
)
filtro_ordem = pn.widgets.Select(
    name="Ordenação",
    options={"Ascendente": "asc", "Descendente": "desc"},
    value="asc"
)
filtro_bar = pn.Row(filtro_nivel, filtro_ordem, margin=10)


def atualizar_filtros(event):
    atualizar_painel()


filtro_nivel.param.watch(atualizar_filtros, 'value')
filtro_ordem.param.watch(atualizar_filtros, 'value')


def set_main_area(area):
    """Define a referência da área principal de exibição."""
    global main_area
    main_area = area


def painel_usuarios():
    user_list = UserController.getAllUsers() or []
    columns = ["id", "nome", "email", "nivelAcesso"]
    df = pd.DataFrame(user_list, columns=columns) if user_list else pd.DataFrame(columns=columns)
    if filtro_nivel.value != "todos":
        df = df[df["nivelAcesso"] == filtro_nivel.value]
    ascending = True if filtro_ordem.value == "asc" else False
    df = df.sort_values("id", ascending=ascending)

    header = pn.Row(
        pn.pane.Markdown("ID", width=50),
        pn.pane.Markdown("Nome", width=150),
        pn.pane.Markdown("Email", width=200),
        pn.pane.Markdown("Nível", width=100),
        pn.pane.Markdown("Ações", width=100)
    )
    linhas = [header]

    for _, row in df.iterrows():
        btn_editar = pn.widgets.Button(name="✏️", width=40)
        btn_excluir = pn.widgets.Button(name="❌", width=40)

        def editar(event, user_id=row["id"]):
            carregar_dados_usuario(user_id)
            if main_area:
                main_area.objects = [pagina_update]

        def excluir(event, user_id=row["id"]):
            UserController.deleteUser(user_id)
            atualizar_painel()

        btn_editar.on_click(editar)
        btn_excluir.on_click(excluir)
        linha = pn.Row(
            pn.pane.Markdown(str(row["id"]), width=50),
            pn.pane.Markdown(row["nome"], width=150),
            pn.pane.Markdown(row["email"], width=200),
            pn.pane.Markdown(str(row["nivelAcesso"]), width=100),
            pn.Row(btn_editar, btn_excluir, width=100),
            margin=5
        )
        linhas.append(linha)

    btn_cadastrar = pn.widgets.Button(name="+ Cadastrar Usuário", button_type="primary", width=200)
    btn_cadastrar.on_click(ir_para_cadastro)

    # Menu lateral com navegação
    btn_usuarios = pn.widgets.Button(name="Usuários", button_type="primary", width=150)
    btn_denuncias = pn.widgets.Button(name="Denúncias", button_type="primary", width=150)
    btn_localizacoes = pn.widgets.Button(name="Localizações", button_type="primary", width=150)

    def goto_usuarios(event):
        if main_area:
            main_area.objects = [painel_usuarios()]

    def goto_denuncias(event):
        import denunciaAdm
        if main_area:
            main_area.objects = [denunciaAdm.painel_denuncias()]

    def goto_localizacoes(event):
        import localizacaoAdm
        if main_area:
            main_area.objects = [localizacaoAdm.painel_localizacoes()]

    btn_usuarios.on_click(goto_usuarios)
    btn_denuncias.on_click(goto_denuncias)
    btn_localizacoes.on_click(goto_localizacoes)

    menu_lateral = pn.Column(
        pn.pane.Markdown("### Menu", align="center"),
        btn_usuarios,
        btn_denuncias,
        btn_localizacoes,
        width=170,
        margin=(10, 10)
    )

    painel = pn.Row(
        menu_lateral,
        pn.Column(
            pn.pane.HTML("<h2 style='font-size:20px'>Painel de Usuários</h2>"),
            btn_cadastrar,
            filtro_bar,
            *linhas,
            margin=10
        )
    )
    painel_centralizado = pn.Row(pn.layout.HSpacer(), painel, pn.layout.HSpacer())
    return painel_centralizado


def atualizar_painel():
    if main_area:
        main_area.objects = [painel_usuarios()]


def ir_para_cadastro(event=None):
    if main_area:
        main_area.objects = [pagina_cadastrar_usuario()]


def pagina_cadastrar_usuario():
    layout = pn.Column(
        pn.pane.Markdown("## Cadastro de Usuário", align="center"),
        input_nome,
        input_email,
        input_senha,
        seletor_nivel,
        pn.Row(btn_confirmar_cadastro, btn_voltar, align="center"),
        mensagem_cadastro,
        align="center",
        width=400
    )
    return layout


def cadastrar_usuario(event=None):
    nome = input_nome.value.strip()
    email = input_email.value.strip()
    senha = input_senha.value.strip()
    nivel = seletor_nivel.value
    if not nome or not email or not senha:
        mensagem_cadastro.object = "❌ Todos os campos são obrigatórios!"
        return
    dados = {
        "nome": nome,
        "email": email,
        "senha": senha,
        "nivelAcesso": int(nivel)
    }
    response = UserController.insertUser(dados)
    if response["status"] == "success":
        mensagem_cadastro.object = "✅ Usuário cadastrado com sucesso!"
        if main_area:
            main_area.objects = [painel_usuarios()]
    else:
        mensagem_cadastro.object = f"❌ Erro: {response['message']}"


def voltar_cadastro(event=None):
    if main_area:
        main_area.objects = [painel_usuarios()]


# Widgets para cadastro de usuário
input_nome = pn.widgets.TextInput(name="Nome")
input_email = pn.widgets.TextInput(name="E-mail")
input_senha = pn.widgets.PasswordInput(name="Senha")
seletor_nivel = pn.widgets.Select(name="Nível de Acesso", options={"1 - Admin": 1, "2 - Usuário Comum": 2})
btn_confirmar_cadastro = pn.widgets.Button(name="Cadastrar", button_type="primary")
btn_voltar = pn.widgets.Button(name="Voltar", button_type="warning")
mensagem_cadastro = pn.pane.Markdown("")

btn_confirmar_cadastro.on_click(cadastrar_usuario)
btn_voltar.on_click(voltar_cadastro)

__all__ = ["painel_usuarios", "set_main_area", "atualizar_painel_callback"]
