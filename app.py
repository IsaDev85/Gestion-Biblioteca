import tkinter as tk
from tkinter import ttk
from collections import deque

AMARILLO  = "#F5C800"
NARANJA   = "#F07800"
GRIS_OSC  = "#4A4A4A"
GRIS_MED  = "#7A7A7A"
GRIS_CLAR = "#F0F0F0"
BLANCO    = "#FFFFFF"
VERDE_OK  = "#2E7D32"

root = tk.Tk()
root.geometry("780x560")
root.title("Biblioteca de Barbosa — IBERO")
root.configure(bg=GRIS_CLAR)
try:
    root.iconbitmap("books.ico")
except:
    pass

users = {}
books = {}
cola_espera = {}
contador_id_user = 1
contador_id_book = 1

style = ttk.Style()
style.theme_use("clam")
style.configure("TNotebook", background=GRIS_CLAR, borderwidth=0)
style.configure("TNotebook.Tab", background=GRIS_MED, foreground=BLANCO,
                font=("Arial", 11, "bold"), padding=[18, 8])
style.map("TNotebook.Tab", background=[("selected", NARANJA)], foreground=[("selected", BLANCO)])
style.configure("TFrame", background=GRIS_CLAR)
style.configure("TCombobox", font=("Arial", 11), fieldbackground=BLANCO)

def lbl(parent, text):
    return tk.Label(parent, text=text, bg=GRIS_CLAR, fg=GRIS_OSC, font=("Arial", 11))

def entry(parent, width=34):
    return tk.Entry(parent, width=width, font=("Arial", 11), bd=1, relief="solid",
                    bg=BLANCO, fg=GRIS_OSC, insertbackground=GRIS_OSC)

def btn(parent, text, command, color="#C8960C", hover="#E6B800"):
    b = tk.Label(parent, text=text, bg=color, fg=BLANCO,
                 font=("Arial", 11, "bold"), cursor="hand2",
                 padx=24, pady=8, relief="flat")
    b.bind("<Button-1>", lambda e: command())
    b.bind("<Enter>",    lambda e: b.config(bg=hover, fg=GRIS_OSC))
    b.bind("<Leave>",    lambda e: b.config(bg=color, fg=BLANCO))
    return b

def make_listbox(parent, height=9):
    frame = tk.Frame(parent, bg=GRIS_CLAR)
    sv = tk.Scrollbar(frame, orient=tk.VERTICAL)
    sh = tk.Scrollbar(frame, orient=tk.HORIZONTAL)
    lb = tk.Listbox(frame, width=56, height=height, font=("Arial", 10),
                    bg=BLANCO, fg=GRIS_OSC, selectbackground=AMARILLO,
                    selectforeground=GRIS_OSC, relief="solid", bd=1,
                    yscrollcommand=sv.set, xscrollcommand=sh.set)
    lb.grid(row=0, column=0, sticky="nsew")
    sv.grid(row=0, column=1, sticky="ns")
    sh.grid(row=1, column=0, sticky="ew")
    sv.config(command=lb.yview)
    sh.config(command=lb.xview)
    frame.grid_rowconfigure(0, weight=1)
    frame.grid_columnconfigure(0, weight=1)
    return frame, lb

def header(parent, text):
    tk.Label(parent, text=text, bg=NARANJA, fg=BLANCO,
             font=("Arial", 13, "bold"), pady=10).pack(fill="x")

status_txt = tk.StringVar(value="  Bienvenido al Sistema de Gestión — Biblioteca de Barbosa")
tk.Label(root, textvariable=status_txt, bg=GRIS_OSC, fg=AMARILLO,
         font=("Arial", 10), anchor="w", pady=4, padx=10).pack(side="bottom", fill="x")

def set_status(msg):
    status_txt.set("  " + msg)

def actualizar_combobox():
    combo_libros["values"] = [
        f"ID {bid}: {b['titulo']} ({'Prestado' if b['prestado'] else 'Libre'})"
        for bid, b in books.items()
    ]

def actualizar_lista_libros():
    lista_libros.delete(0, tk.END)
    for bid, b in books.items():
        estado = "● Ocupado" if b["prestado"] else "● Libre"
        lista_libros.insert(tk.END,
            f"  ID {bid:03d}   {b['titulo']} — {b['autor']}  [{b['genero']}]  {estado}")

def guardar_usuario():
    global contador_id_user
    nombre = entrada_nombre.get().strip()
    apellido = entrada_apellido.get().strip()
    if nombre and apellido:
        users[contador_id_user] = {"nombre": nombre, "apellido": apellido}
        lista_usuarios.insert(tk.END, f"  ID {contador_id_user:03d}   {nombre} {apellido}")
        combo_usuarios["values"] = [f"ID {uid}: {u['nombre']} {u['apellido']}" for uid, u in users.items()]
        entrada_nombre.delete(0, tk.END)
        entrada_apellido.delete(0, tk.END)
        set_status(f"✔  Usuario '{nombre} {apellido}' registrado.")
        contador_id_user += 1
    else:
        set_status("⚠  Completa nombre y apellido.")

def guardar_libro():
    global contador_id_book
    titulo = entrada_titulo.get().strip()
    autor  = entrada_autor.get().strip()
    genero = entrada_genero.get().strip()
    if titulo and autor and genero:
        books[contador_id_book] = {"titulo": titulo, "autor": autor, "genero": genero,
                                    "prestado": False, "usuario": None}
        cola_espera[contador_id_book] = deque()
        actualizar_lista_libros()
        actualizar_combobox()
        entrada_titulo.delete(0, tk.END)
        entrada_autor.delete(0, tk.END)
        entrada_genero.delete(0, tk.END)
        set_status(f"✔  Libro '{titulo}' registrado.")
        contador_id_book += 1
    else:
        set_status("⚠  Completa todos los campos.")

def prestar_libro():
    libro_txt   = combo_libros.get()
    usuario_txt = combo_usuarios.get()
    if libro_txt and usuario_txt:
        libro_id   = int(libro_txt.split()[1].strip(":"))
        usuario_id = int(usuario_txt.split()[1].strip(":"))
        if not books[libro_id]["prestado"]:
            books[libro_id]["prestado"] = True
            books[libro_id]["usuario"]  = usuario_id
            actualizar_combobox()
            actualizar_lista_libros()
            lista_prestados.insert(tk.END,
                f"  {users[usuario_id]['nombre']} {users[usuario_id]['apellido']}  →  {books[libro_id]['titulo']}")
            set_status(f"✔  Préstamo registrado correctamente.")
            combo_libros.set("")
            combo_usuarios.set("")
        else:
            cola_espera[libro_id].append(usuario_id)
            lista_espera.insert(tk.END,
                f"  {users[usuario_id]['nombre']}  esperando  '{books[libro_id]['titulo']}'")
            set_status(f"ℹ  Libro no disponible. Usuario agregado a la cola.")
    else:
        set_status("⚠  Selecciona usuario y libro.")

def devolver_libro():
    sel = lista_prestados.curselection()
    if sel:
        texto = lista_prestados.get(sel)
        libro_titulo = texto.split("→")[1].strip()
        libro_id = next((bid for bid, b in books.items() if b["titulo"] == libro_titulo), None)
        if libro_id:
            if cola_espera[libro_id]:
                sig = cola_espera[libro_id].popleft()
                books[libro_id]["usuario"] = sig
                lista_prestados.delete(sel)
                lista_prestados.insert(sel,
                    f"  {users[sig]['nombre']} {users[sig]['apellido']}  →  {books[libro_id]['titulo']}")
                for i in range(lista_espera.size()):
                    if users[sig]["nombre"] in lista_espera.get(i):
                        lista_espera.delete(i); break
                set_status(f"✔  Asignado desde la cola correctamente.")
            else:
                books[libro_id]["prestado"] = False
                books[libro_id]["usuario"]  = None
                lista_prestados.delete(sel)
                actualizar_lista_libros()
                set_status(f"✔  Libro devuelto correctamente.")
            actualizar_combobox()
    else:
        set_status("⚠  Selecciona un préstamo activo.")

# ── Notebook ──────────────────────────────────────────────────
nb = ttk.Notebook(root)
tab1 = ttk.Frame(nb); tab2 = ttk.Frame(nb)
tab3 = ttk.Frame(nb); tab4 = ttk.Frame(nb)
nb.add(tab1, text="  👤 Usuarios  ")
nb.add(tab2, text="  📚 Libros  ")
nb.add(tab3, text="  🔄 Préstamos  ")
nb.add(tab4, text="  📋 Activos  ")
nb.pack(expand=True, fill="both", padx=10, pady=(10, 0))

# Tab 1
header(tab1, "Registro de Usuarios")
form1 = tk.Frame(tab1, bg=GRIS_CLAR); form1.pack(pady=14)
lbl(form1, "Nombre:").grid(row=0, column=0, sticky="e", padx=8, pady=5)
entrada_nombre = entry(form1); entrada_nombre.grid(row=0, column=1, padx=8, pady=5)
lbl(form1, "Apellido:").grid(row=1, column=0, sticky="e", padx=8, pady=5)
entrada_apellido = entry(form1); entrada_apellido.grid(row=1, column=1, padx=8, pady=5)
btn(tab1, "Guardar Usuario", guardar_usuario).pack(pady=8)
f1, lista_usuarios = make_listbox(tab1)
f1.pack(padx=14, pady=4, fill="both", expand=True)

# Tab 2
header(tab2, "Registro de Libros")
form2 = tk.Frame(tab2, bg=GRIS_CLAR); form2.pack(pady=14)
lbl(form2, "Título:").grid(row=0, column=0, sticky="e", padx=8, pady=5)
entrada_titulo = entry(form2); entrada_titulo.grid(row=0, column=1, padx=8, pady=5)
lbl(form2, "Autor:").grid(row=1, column=0, sticky="e", padx=8, pady=5)
entrada_autor = entry(form2); entrada_autor.grid(row=1, column=1, padx=8, pady=5)
lbl(form2, "Género:").grid(row=2, column=0, sticky="e", padx=8, pady=5)
entrada_genero = entry(form2); entrada_genero.grid(row=2, column=1, padx=8, pady=5)
btn(tab2, "Guardar Libro", guardar_libro).pack(pady=8)
f2, lista_libros = make_listbox(tab2)
f2.pack(padx=14, pady=4, fill="both", expand=True)

# Tab 3
header(tab3, "Gestión de Préstamos")
form3 = tk.Frame(tab3, bg=GRIS_CLAR); form3.pack(pady=14)
lbl(form3, "Usuario:").grid(row=0, column=0, sticky="e", padx=8, pady=5)
combo_usuarios = ttk.Combobox(form3, width=38, state="readonly", font=("Arial", 11))
combo_usuarios.grid(row=0, column=1, padx=8, pady=5)
lbl(form3, "Libro:").grid(row=1, column=0, sticky="e", padx=8, pady=5)
combo_libros = ttk.Combobox(form3, width=38, state="readonly", font=("Arial", 11))
combo_libros.grid(row=1, column=1, padx=8, pady=5)
btn(tab3, "Prestar Libro", prestar_libro).pack(pady=8)
lbl(tab3, "Cola de espera:").pack()
f3e, lista_espera = make_listbox(tab3, height=5)
f3e.pack(padx=14, pady=4, fill="both", expand=True)

# Tab 4
header(tab4, "Préstamos Activos")
f4, lista_prestados = make_listbox(tab4, height=12)
f4.pack(padx=14, pady=14, fill="both", expand=True)
b_dev = btn(tab4, "Devolver Libro", devolver_libro, color=VERDE_OK, hover="#43A047")
b_dev.pack(pady=8)

root.mainloop()
