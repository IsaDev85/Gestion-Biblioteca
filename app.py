import tkinter as tk
from tkinter import ttk
from collections import deque

root = tk.Tk()
root.geometry("700x500")
root.iconbitmap("books.ico")
root.title("Biblioteca de Barbosa")

users = {}
books = {}
cola_espera = {}
contador_id_user = 1
contador_id_book = 1


def guardar_usuario():
    global contador_id_user
    nombre = entrada_nombre.get()
    apellido = entrada_apellido.get()
    if nombre and apellido:
        users[contador_id_user] = {"nombre": nombre, "apellido": apellido}
        lista_usuarios.insert(tk.END, f"ID {contador_id_user}: {nombre} {apellido}")
        combo_usuarios["values"] = [
            f"ID {uid}: {u['nombre']} {u['apellido']}" for uid, u in users.items()
        ]
        entrada_nombre.delete(0, tk.END)
        entrada_apellido.delete(0, tk.END)
        contador_id_user += 1


def guardar_libro():
    global contador_id_book
    titulo = entrada_titulo.get()
    autor = entrada_autor.get()
    genero = entrada_genero.get()
    if titulo and autor and genero:
        books[contador_id_book] = {
            "titulo": titulo,
            "autor": autor,
            "genero": genero,
            "prestado": False,
            "usuario": None,
        }
        cola_espera[contador_id_book] = deque()
        texto = f"ID {contador_id_book}: {titulo} - {autor} ({genero}) [Libre]"
        lista_libros.insert(tk.END, texto)
        combo_libros["values"] = [
            f"ID {bid}: {b['titulo']} ({'Prestado' if b['prestado'] else 'Libre'})"
            for bid, b in books.items()
        ]
        entrada_titulo.delete(0, tk.END)
        entrada_autor.delete(0, tk.END)
        entrada_genero.delete(0, tk.END)
        contador_id_book += 1


def prestar_libro():
    libro_texto = combo_libros.get()
    usuario_texto = combo_usuarios.get()
    if libro_texto and usuario_texto:
        libro_id = int(libro_texto.split()[1].strip(":"))
        usuario_id = int(usuario_texto.split()[1].strip(":"))

        if not books[libro_id]["prestado"]:
            books[libro_id]["prestado"] = True
            books[libro_id]["usuario"] = usuario_id
            actualizar_combobox()
            lista_prestados.insert(
                tk.END, f"{users[usuario_id]['nombre']} → {books[libro_id]['titulo']}"
            )
        else:
            cola_espera[libro_id].append(usuario_id)
            lista_espera.insert(
                tk.END,
                f"{users[usuario_id]['nombre']} esperando {books[libro_id]['titulo']}",
            )


def devolver_libro():
    seleccion = lista_prestados.curselection()
    if seleccion:
        texto = lista_prestados.get(seleccion)
        libro_titulo = texto.split("→")[1].strip()
        libro_id = next(
            (bid for bid, b in books.items() if b["titulo"] == libro_titulo), None
        )
        if libro_id:
            if cola_espera[libro_id]:
                siguiente_usuario = cola_espera[libro_id].popleft()
                books[libro_id]["usuario"] = siguiente_usuario
                lista_prestados.delete(seleccion)
                lista_prestados.insert(
                    seleccion,
                    f"{users[siguiente_usuario]['nombre']} → {books[libro_id]['titulo']}",
                )
            else:
                books[libro_id]["prestado"] = False
                books[libro_id]["usuario"] = None
                lista_prestados.delete(seleccion)
            actualizar_combobox()


def actualizar_combobox():
    combo_libros["values"] = [
        f"ID {bid}: {b['titulo']} ({'Prestado' if b['prestado'] else 'Libre'})"
        for bid, b in books.items()
    ]


notebook = ttk.Notebook(root)
tab1 = ttk.Frame(notebook)
tab2 = ttk.Frame(notebook)
tab3 = ttk.Frame(notebook)
tab4 = ttk.Frame(notebook)
notebook.add(tab1, text="Registro de Usuario")
notebook.add(tab2, text="Registro de Libros")
notebook.add(tab3, text="Prestar libro")
notebook.add(tab4, text="Libros Prestados")
notebook.pack(expand=True, fill="both")

tk.Label(tab1, text="Nombre:").pack()
entrada_nombre = tk.Entry(tab1, width=30)
entrada_nombre.pack(pady=5)

tk.Label(tab1, text="Apellido:").pack()
entrada_apellido = tk.Entry(tab1, width=30)
entrada_apellido.pack(pady=5)

boton_usuario = tk.Button(tab1, text="Guardar Usuario", command=guardar_usuario)
boton_usuario.pack(pady=10)

lista_usuarios = tk.Listbox(tab1, width=50, height=10)
lista_usuarios.pack(pady=10)

tk.Label(tab2, text="Título:").pack()
entrada_titulo = tk.Entry(tab2, width=30)
entrada_titulo.pack(pady=5)

tk.Label(tab2, text="Autor:").pack()
entrada_autor = tk.Entry(tab2, width=30)
entrada_autor.pack(pady=5)

tk.Label(tab2, text="Género:").pack()
entrada_genero = tk.Entry(tab2, width=30)
entrada_genero.pack(pady=5)

boton_libro = tk.Button(tab2, text="Guardar Libro", command=guardar_libro)
boton_libro.pack(pady=10)

lista_libros = tk.Listbox(tab2, width=50, height=10)
lista_libros.pack(pady=10)

tk.Label(tab3, text="Seleccionar Usuario:").pack()
combo_usuarios = ttk.Combobox(tab3, width=40, state="readonly")
combo_usuarios.pack(pady=5)

tk.Label(tab3, text="Seleccionar Libro:").pack()
combo_libros = ttk.Combobox(tab3, width=40, state="readonly")
combo_libros.pack(pady=5)

boton_prestar = tk.Button(tab3, text="Prestar Libro", command=prestar_libro)
boton_prestar.pack(pady=10)

tk.Label(tab3, text="Cola de espera:").pack()
lista_espera = tk.Listbox(tab3, width=50, height=5)
lista_espera.pack(pady=10)

lista_prestados = tk.Listbox(tab4, width=50, height=10)
lista_prestados.pack(pady=10)

boton_devolver = tk.Button(tab4, text="Devolver Libro", command=devolver_libro)
boton_devolver.pack(pady=10)

root.mainloop()
