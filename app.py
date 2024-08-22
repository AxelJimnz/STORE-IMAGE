import sqlite3
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk

# Función para abrir una ventana y subir una imagen
def upload_image():
    file_path = filedialog.askopenfilename(title="Selecciona una imagen", filetypes=[("Image files", "*.jpg *.png *.jpeg")])
    if file_path:
        image_name = file_path.split('/')[-1]
        conn = sqlite3.connect('image_app.db')
        cursor = conn.cursor()
        cursor.execute("INSERT INTO images (image_name, image_path) VALUES (?, ?)", (image_name, file_path))
        conn.commit()
        conn.close()
        refresh_image_list()

# Función para eliminar una imagen seleccionada
def delete_image():
    selected_item = image_listbox.curselection()
    if selected_item:
        image_name = image_listbox.get(selected_item)
        conn = sqlite3.connect('image_app.db')
        cursor = conn.cursor()
        cursor.execute("DELETE FROM images WHERE image_name=?", (image_name,))
        conn.commit()
        conn.close()
        refresh_image_list()

# Función para mostrar la imagen seleccionada en el canvas
def show_image():
    selected_item = image_listbox.curselection()
    if selected_item:
        image_name = image_listbox.get(selected_item)
        conn = sqlite3.connect('image_app.db')
        cursor = conn.cursor()
        cursor.execute("SELECT image_path FROM images WHERE image_name=?", (image_name,))
        image_path = cursor.fetchone()[0]
        conn.close()

        # Cargar y redimensionar la imagen para que se ajuste al canvas
        img = Image.open(image_path)
        img.thumbnail((300, 300))  # Redimensionar imagen al tamaño del canvas
        img = ImageTk.PhotoImage(img)

        # Limpiar el canvas antes de mostrar la nueva imagen
        canvas.image = img  # Mantener la referencia a la imagen para evitar que se borre
        canvas.create_image(150, 150, anchor=tk.CENTER, image=img)

# Función para actualizar la lista de imágenes
def refresh_image_list():
    image_listbox.delete(0, tk.END)
    conn = sqlite3.connect('image_app.db')
    cursor = conn.cursor()
    cursor.execute("SELECT image_name FROM images")
    images = cursor.fetchall()
    for image in images:
        image_listbox.insert(tk.END, image[0])
    conn.close()

# Ventana principal con un diseño más bonito
def open_main_window():
    main_window = tk.Tk()
    main_window.title("Gestión de Imágenes")
    main_window.geometry("500x400")
    main_window.config(bg="#f0f0f0")

    # Frame para el listado de imágenes
    left_frame = tk.Frame(main_window, bg="#f0f0f0", padx=10, pady=10)
    left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    right_frame = tk.Frame(main_window, bg="#ffffff", padx=10, pady=10)
    right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

    # Botones de acciones
    upload_button = tk.Button(left_frame, text="Subir Imagen", command=upload_image, bg="#4CAF50", fg="white", padx=10, pady=5)
    upload_button.pack(pady=5, fill=tk.X)

    delete_button = tk.Button(left_frame, text="Eliminar Imagen", command=delete_image, bg="#f44336", fg="white", padx=10, pady=5)
    delete_button.pack(pady=5, fill=tk.X)

    show_button = tk.Button(left_frame, text="Ver Imagen", command=show_image, bg="#2196F3", fg="white", padx=10, pady=5)
    show_button.pack(pady=5, fill=tk.X)

    # Lista de imágenes
    global image_listbox
    image_listbox = tk.Listbox(left_frame, height=15, bg="#ffffff", fg="#000000")
    image_listbox.pack(pady=10, fill=tk.BOTH, expand=True)

    refresh_image_list()

    # Canvas para mostrar la imagen seleccionada
    global canvas
    canvas = tk.Canvas(right_frame, width=300, height=300, bg="#e0e0e0")
    canvas.pack(padx=10, pady=10)

    # Título en el canvas
    #label_title = tk.Label(right_frame, text="Imagen seleccionada", bg="#ffffff", font=("Arial", 12))
    #label_title.pack()

    main_window.mainloop()

# Ejecutar la aplicación
open_main_window()
