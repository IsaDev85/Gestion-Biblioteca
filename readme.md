# 📚 Biblioteca de Barbosa

Aplicación en **Python + Tkinter** para la gestión de usuarios y libros en una biblioteca.  
Permite registrar usuarios, registrar libros, prestar libros y manejar una cola de espera cuando un libro ya está prestado.

---

## 🚀 Funcionalidades

### 1. Registro de Usuarios
- Se ingresan **nombre** y **apellido**.
- Cada usuario recibe un **ID autogenerado**.
- Los usuarios se muestran en una lista y en un **combobox** para seleccionarlos al momento de prestar libros.

### 2. Registro de Libros
- Se ingresan **título**, **autor** y **género**.
- Cada libro recibe un **ID autogenerado**.
- Los libros se muestran en una lista y en un **combobox** con su estado inicial: **[Libre]**.

### 3. Préstamo de Libros
- En la pestaña de préstamos se selecciona:
  - Un **usuario** desde el combobox.
  - Un **libro** desde el combobox.
- Si el libro está **libre**, se presta al usuario y cambia su estado a **[Prestado a Usuario]**.
- Si el libro ya está **prestado**, el nuevo usuario se agrega automáticamente a una **cola de espera** que se muestra en la interfaz.

### 4. Gestión de Libros Prestados
- En la pestaña de libros prestados se muestra qué usuario tiene cada libro.
- Al devolver un libro:
  - Si hay usuarios en la cola de espera, el primero recibe el préstamo automáticamente.
  - Si no hay cola, el libro vuelve a estado **[Libre]**.

---

## 🧩 Flujo de Uso

1. **Registrar usuarios** en la pestaña 1.  
2. **Registrar libros** en la pestaña 2.  
3. **Prestar libros** en la pestaña 3 seleccionando usuario y libro.  
   - Si está libre → se presta.  
   - Si está ocupado → el usuario entra en la cola de espera.  
4. **Ver y devolver préstamos** en la pestaña 4.  
   - Al devolver, el siguiente usuario en la cola recibe el libro automáticamente.  

---

## 📌 Ejemplo de interacción

- Registrar **Usuario A** y **Usuario B**.  
- Registrar el libro **“Cien años de soledad”**.  
- Prestar el libro a **Usuario A** → aparece en pestaña 4:  

- Intentar prestarlo a **Usuario B** mientras aún lo tiene A → aparece en la cola de espera:  


- Al devolver el libro → automáticamente pasa a Usuario B y se actualiza la lista.

---

## ⚙️ Tecnologías usadas
- Python 3.x  
- Tkinter (interfaz gráfica)  
- `ttk.Notebook` para pestañas  
- `deque` de `collections` para manejar la cola de espera  

---

## 📖 Próximas mejoras
- Mostrar detalles completos del libro (título, autor, género, estado, usuario actual) en la pestaña de préstamos.  
- Exportar registros a archivo CSV o base de datos.  
- Implementar búsqueda y filtrado de usuarios/libros.
