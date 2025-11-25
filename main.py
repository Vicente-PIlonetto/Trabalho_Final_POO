import asyncio
import tkinter as tk
from typing import Optional

from views import Login_view, Sign_up_view
from views.cadastros.produto import Cadastro_produto_view
from views.carrinho import Carrinho_view
from views.compras import Compra_view
from views.compras_apenas import Compras_apenas_view
from views.index import Index_view

APP_NAME = "AAAAAA"


def change_view(pwd: str, *args):
    global wpd, current_view
    local = None

    if current_view:
        current_view.destroy()
        current_view = None

    match pwd:
        case "/sign_up":
            current_view = Sign_up_view(root, lambda: change_view("/login"))
            local = "Sign up"
        case "/login":
            current_view = Login_view(
                root,
                lambda: change_view("/sign_up"),
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
            current_view = Index_view(root, args[0], change_view)
            local = "Index"
        case "/pagamento":
            current_view = Index_view(root, args[0], change_view)
            local = "Pagamento"
        case "/cadastro_produto":
            current_view = Cadastro_produto_view(root, args[0], change_view)
            local = "Cadastro de produtos"

    root.wm_title(f"{APP_NAME} - {local}")
    if not current_view:
        current_view = tk.Frame(root)
        tk.Label(root, text="Nenhuma Rota!").pack(expand=True)
    else:
        current_view.pack()


def close():
    global runnig
    runnig = False


pwd = None
runnig = True

root = tk.Tk()

current_view: Optional[tk.Frame] = None
change_view("/login")

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
