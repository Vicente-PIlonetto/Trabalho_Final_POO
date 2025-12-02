import asyncio
import tkinter as tk
from typing import Optional

from globals import INFOS_PADAO
from views import Login_view, Sign_up_view
from views.cadastros.produto import Cadastro_produto_view
from views.carrinho import Carrinho_view
from views.compras import Compra_view
from views.compras_apenas import Compras_apenas_view
from views.index import Index_view
from database import run_init
from views.pedidos import Pedidos_view

asyncio.run(run_init())

APP_NAME = "True Joja"


def change_view(pwd: str, *args):
    global wpd, current_view
    local = None

    if current_view:
        current_view.destroy()
        current_view = None

    match pwd:
        case "/sign_up":
            current_view = Sign_up_view(root, lambda: change_view("/login") if INFOS_PADAO["primeiro_usuario"] else change_view("/index", args[0]))
            local = "Sign up"
        case "/login":
            current_view = Login_view(
                root,
                lambda user: change_view("/index", user),
            )
            local = "Login"
        case "/compras":
            local = "Compras"
            if args[0] == None:
                current_view = Compra_view(root, args[1], change_view)
            else:
                current_view = Compras_apenas_view(root, args[0], args[1], change_view)
            local = "Login"
        case "/carrinho":
            current_view = Carrinho_view(root, args[0], change_view)
            local = "Carrinho"
        case "/index":
            INFOS_PADAO["primeiro_usuario"] = False
            current_view = Index_view(root, args[0], change_view)
            local = "Index"
        case "/pagamento":
            current_view = Index_view(root, args[0], change_view)
            local = "Pagamento"
        case "/cadastro_produto":
            current_view = Cadastro_produto_view(root, args[0], change_view)
            local = "Cadastro de produtos"
        case "/pedidos":
            current_view = Pedidos_view(root, args[0], change_view)
            local = "Pedidos"

    root.wm_title(f"{APP_NAME} - {local}")
    root.minsize(int(len(f"{APP_NAME} - {local}") + 220), 0)
    if not current_view:
        current_view = tk.Frame(root)
        tk.Label(root, text="Nenhuma Rota!").pack(expand=True)
        tk.Button(root, text="Voltar", command=lambda*args:change_view("/index", args[0])).pack(expand=True)
    else:
        current_view.pack()


def close():
    global runnig
    runnig = False


pwd = None
runnig = True

root = tk.Tk()

current_view: tk.Frame | None = None

change_view("/sign_up" if INFOS_PADAO["primeiro_usuario"] else "/login")

root.protocol("WM_DELETE_WINDOW", close)


async def main_loop():
    try:
        while runnig:
            root.update()
            await asyncio.sleep(0.01)
        root.destroy()
    except tk.TclError:
        pass


asyncio.run(main_loop())
