import tkinter as tk
from tkinter import colorchooser

def escolher_cor():
    cor = colorchooser.askcolor(title="Escolha uma cor")
    print(cor)  # retorna ((R, G, B), "#rrggbb")
    if cor[1]:  # cor[1] é a representação hexadecimal
        label.config(bg=cor[1])

root = tk.Tk()
root.geometry("300x100")

btn = tk.Button(root, text="Escolher cor", command=escolher_cor)
btn.pack(pady=10)

label = tk.Label(root, text="Veja a cor aqui", width=20)
label.pack(pady=10)

root.mainloop()
