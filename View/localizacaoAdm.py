import panel as pn
import pandas as pd
from Controller.localizacaoController import LocalizacaoController
from localizacaoUpdate import carregar_dados_localizacao, pagina_update as localizacao_update_page
from localizacaoCadastro import pagina_cadastrar_localizacao

main_area = None


def set_main_area(area):
    global main_area
    main_area = area


def painel_localizacoes():
    local_list = LocalizacaoController.getAllLocalizacoes() or []
    columns = ["id", "nome"]
    df = pd.DataFrame(local_list, columns=columns) if local_list else pd.DataFrame(columns=columns)
    df = df.sort_values("id", ascending=True)

    header = pn.Row(
        pn.pane.Markdown("ID", width=50),
        pn.pane.Markdown("Nome", width=200),
        pn.pane.Markdown("Ações", width=100)
    )
    linhas = [header]

    for _, row in df.iterrows():
        btn_editar = pn.widgets.Button(name="✏️", width=40)
        btn_excluir = pn.widgets.Button(name="❌", width=40)

        def editar(event, local_id=row["id"]):
            carregar_dados_localizacao(local_id)
            if main_area:
                main_area.objects = [localizacao_update_page]

        def excluir(event, local_id=row["id"]):
            LocalizacaoController.deleteLocalizacao(local_id)
            atualizar_painel()

        btn_editar.on_click(editar)
        btn_excluir.on_click(excluir)
        linha = pn.Row(
            pn.pane.Markdown(str(row["id"]), width=50),
            pn.pane.Markdown(row["nome"], width=200),
            pn.Row(btn_editar, btn_excluir, width=100),
            margin=5
        )
        linhas.append(linha)

    btn_cadastrar = pn.widgets.Button(name="+ Cadastrar Localização", button_type="primary", width=200)
    btn_cadastrar.on_click(ir_para_cadastro)

    # Menu lateral com navegação
    btn_usuarios = pn.widgets.Button(name="Usuários", button_type="primary", width=150)
    btn_denuncias = pn.widgets.Button(name="Denúncias", button_type="primary", width=150)
    btn_localizacoes = pn.widgets.Button(name="Localizações", button_type="primary", width=150)

    def goto_usuarios(event):
        import userAdm
        if main_area:
            main_area.objects = [userAdm.painel_usuarios()]

    def goto_denuncias(event):
        import denunciaAdm
        if main_area:
            main_area.objects = [denunciaAdm.painel_denuncias()]

    def goto_localizacoes(event):
        if main_area:
            main_area.objects = [painel_localizacoes()]

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
            pn.pane.HTML("<h2 style='font-size:20px'>Painel de Localizações</h2>"),
            btn_cadastrar,
            *linhas,
            margin=10,
            align="center"
        )
    )
    painel_centralizado = pn.Row(pn.layout.HSpacer(), painel, pn.layout.HSpacer())
    return painel_centralizado


def atualizar_painel():
    if main_area:
        main_area.objects = [painel_localizacoes()]


def ir_para_cadastro(event=None):
    if main_area:
        main_area.objects = [pagina_cadastrar_localizacao()]


__all__ = ["painel_localizacoes", "set_main_area"]
