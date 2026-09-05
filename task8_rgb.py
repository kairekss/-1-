# -*- coding: utf-8 -*-
"""
ЗАДАНИЕ 9: RGB палитра
"""

import tkinter as tk

root = tk.Tk()
root.title("Задание 9: RGB Палитра")
root.geometry("500x500")
root.configure(bg='#1a1a2e')


# Функция обновления цвета при движении слайдеров
def update_color(value=None):
    # Получаем значения R, G, B (0-255)
    r = trackbar_r.get()
    g = trackbar_g.get()
    b = trackbar_b.get()
    # Формируем HEX-код: #RRGGBB (каждый по 2 символа)
    hex_color = f"#{r:02x}{g:02x}{b:02x}"

    # Меняем цвет превью
    color_preview.config(bg=hex_color)
    # Обновляем текстовые метки с кодом цвета
    label_hex.config(text=f"HEX: {hex_color.upper()}")
    label_rgb.config(text=f"RGB: ({r}, {g}, {b})")


# --- Слайдер R (Красный) ---
tk.Label(root, text="R (Красный)", fg='#ff6b6b', bg='#1a1a2e',
         font=('Arial', 10, 'bold')).pack()
trackbar_r = tk.Scale(root, from_=0, to=255, orient=tk.HORIZONTAL,
                      length=400, command=update_color,
                      bg='#1a1a2e', fg='#ff6b6b',
                      troughcolor='#2d2d44', sliderlength=20)
trackbar_r.set(128)  # Начальное значение
trackbar_r.pack()

# --- Слайдер G (Зелёный) ---
tk.Label(root, text="G (Зелёный)", fg='#6bffb8', bg='#1a1a2e',
         font=('Arial', 10, 'bold')).pack()
trackbar_g = tk.Scale(root, from_=0, to=255, orient=tk.HORIZONTAL,
                      length=400, command=update_color,
                      bg='#1a1a2e', fg='#6bffb8',
                      troughcolor='#2d2d44', sliderlength=20)
trackbar_g.set(128)
trackbar_g.pack()

# --- Слайдер B (Синий) ---
tk.Label(root, text="B (Синий)", fg='#6bcbff', bg='#1a1a2e',
         font=('Arial', 10, 'bold')).pack()
trackbar_b = tk.Scale(root, from_=0, to=255, orient=tk.HORIZONTAL,
                      length=400, command=update_color,
                      bg='#1a1a2e', fg='#6bcbff',
                      troughcolor='#2d2d44', sliderlength=20)
trackbar_b.set(128)
trackbar_b.pack()

# --- Превью цвета ---
# height, width - размеры в символах, bg - начальный цвет
color_preview = tk.Label(root, text="  ", bg="#808080", height=3, width=30)
color_preview.pack(pady=10)

# --- Информация о цвете ---
label_hex = tk.Label(root, text="HEX: #808080", font=('Consolas', 12, 'bold'),
                     fg='#00d4ff', bg='#1a1a2e')
label_hex.pack()

label_rgb = tk.Label(root, text="RGB: (128, 128, 128)",
                     font=('Consolas', 12, 'bold'),
                     fg='#ff6b9d', bg='#1a1a2e')
label_rgb.pack()

# Инициализация цвета при старте
update_color()
root.mainloop()