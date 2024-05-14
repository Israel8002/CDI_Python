import tkinter as tk

def create_window():
    window = tk.Tk()
    window.title("Ventana con Grid")
    window.geometry("400x300")
    window.configure(bg="#363636")  # Color de fondo negro
    
    # Borde redondeado
    window.attributes('-alpha', 0.9)
    window.attributes('-transparentcolor', '#363636')

    # Cuadrícula
    for i in range(5):
        for j in range(3):
            tk.Label(window, text=f"Row {i}, Col {j}", bg="#363636", fg="white").grid(row=i+1, column=j, padx=10, pady=10)
    
    window.mainloop()

create_window()
