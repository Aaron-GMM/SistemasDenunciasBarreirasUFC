import panel as pn
import pandas as pd
from Controller.denunciaController import DenunciaController
from denunciaUpdate import carregar_dados_denuncia, pagina_update as denuncia_update_page
from denunciaCadastro import pagina_cadastrar_denuncia

main_area = None  # Será definido via set_main_area
atualizar_painel_callback = None


def set_main_area(area):
    global main_area
    main_area = area


def painel_denuncias():
    denuncia_list = DenunciaController.getAllDenuncias() or []
    columns = ["id", "titulo", "descricao", "ponto_referencia", "idcategoria", "idstatus", "idusuario", "idlocalizacao"]
    df = pd.DataFrame(denuncia_list, columns=columns) if denuncia_list else pd.DataFrame(columns=columns)
    df = df.sort_values("id", ascending=True)

    header = pn.Row(
        pn.pane.Markdown("ID", width=50),
        pn.pane.Markdown("Título", width=150),
        pn.pane.Markdown("Descrição", width=200),
        pn.pane.Markdown("Ponto de Ref.", width=150),
        pn.pane.Markdown("Categoria", width=100),
        pn.pane.Markdown("Status", width=100),
        pn.pane.Markdown("Usuário", width=100),
        pn.pane.Markdown("Localização", width=100),
        pn.pane.Markdown("Ações", width=100)
    )
    linhas = [header]

    for _, row in df.iterrows():
        btn_editar = pn.widgets.Button(name="✏️", width=40)
        btn_excluir = pn.widgets.Button(name="❌", width=40)

        def editar(event, denuncia_id=row["id"]):
            carregar_dados_denuncia(denuncia_id)
            if main_area:
                main_area.objects = [denuncia_update_page]

        def excluir(event, denuncia_id=row["id"]):
            DenunciaController.deleteDenuncia(denuncia_id)
            atualizar_painel()

        btn_editar.on_click(editar)
        btn_excluir.on_click(excluir)
        linha = pn.Row(
            pn.pane.Markdown(str(row["id"]), width=50),
            pn.pane.Markdown(row["titulo"], width=150),
            pn.pane.Markdown(row["descricao"], width=200),
            pn.pane.Markdown(row["ponto_referencia"], width=150),
            pn.pane.Markdown(str(row["idcategoria"]), width=100),
            pn.pane.Markdown(str(row["idstatus"]), width=100),
            pn.pane.Markdown(str(row["idusuario"]), width=100),
            pn.pane.Markdown(str(row["idlocalizacao"]), width=100),
            pn.Row(btn_editar, btn_excluir, width=100),
            margin=5
        )
        linhas.append(linha)

    btn_cadastrar = pn.widgets.Button(name="+ Cadastrar Denúncia", button_type="primary", width=200)
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
        if main_area:
            main_area.objects = [painel_denuncias()]

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
            pn.pane.HTML("<h2 style='font-size:20px'>Painel de Denúncias</h2>"),
            btn_cadastrar,
            *linhas,
            margin=10
        )
    )
    painel_centralizado = pn.Row(pn.layout.HSpacer(), painel, pn.layout.HSpacer())
    return painel_centralizado


def atualizar_painel():
    if main_area:
        main_area.objects = [painel_denuncias()]


def ir_para_cadastro(event=None):
    if main_area:
        main_area.objects = [pagina_cadastrar_denuncia()]


__all__ = ["painel_denuncias", "set_main_area", "atualizar_painel_callback"]
