import tkinter as tk
from tkinter import ttk

def on_select():
    selected_items = tree.selection()  # retorna IDs dos itens selecionados
    for item_id in selected_items:
        values = tree.item(item_id)['values']  # pega os valores da linha
        print("Linha selecionada:", values)

root = tk.Tk()

tree = ttk.Treeview(root, columns=("Nome", "Idade"), show="headings")
tree.heading("Nome", text="Nome")
tree.heading("Idade", text="Idade")
tree.pack()

tree.insert("", tk.END, values=("Alice", 25))
tree.insert("", tk.END, values=("Bob", 30))

btn = tk.Button(root, text="Selecionar", command=on_select)
btn.pack()

root.mainloop()
