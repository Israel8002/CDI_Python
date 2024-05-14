import tkinter as tk
from PIL import Image, ImageDraw, ImageTk

def round_corner(radius):
    """Genera una imagen con esquinas redondeadas."""
    width = radius * 2
    image = Image.new('RGBA', (width, width), (0, 0, 0, 0))
    draw = ImageDraw.Draw(image)
    draw.ellipse((0, 0, width, width), fill=(255, 255, 255, 255))
    return image

def rounded_label(parent, text, radius=10, **kwargs):
    """Crea un Label con esquinas redondeadas."""
    label = tk.Label(parent, text=text, **kwargs)
    label_image = round_corner(radius)
    label.img = ImageTk.PhotoImage(label_image)
    label.config(image=label.img, compound=tk.CENTER)
    return label

# Crear ventana
root = tk.Tk()
root.geometry("300x200")

# Crear label con esquinas redondeadas
rounded_label = rounded_label(root, text="Hola mundo!", radius=20)
rounded_label.pack(pady=20)

root.mainloop()
