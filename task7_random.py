# -*- coding: utf-8 -*-
"""
ЗАДАНИЕ 8: Случайные числа + Сброс
"""

import tkinter as tk
from tkinter import ttk, messagebox
import random  # для генерации случайных чисел

root = tk.Tk()
root.title("Задание 8: Случайные числа")
root.geometry("450x400")
root.configure(bg='#1a1a2e')

# ProgressBar для отображения случайного числа
progress = ttk.Progressbar(root, length=350, mode='determinate', maximum=100)
progress.pack(pady=15)

# --- Слайдер MIN ---
tk.Label(root, text="Min:", fg='#ff6b6b', bg='#1a1a2e',
        font=('Arial', 10, 'bold')).pack()
trackbar_min = tk.Scale(root, from_=0, to=100, orient=tk.HORIZONTAL,
                       length=350, bg='#1a1a2e', fg='#ff6b6b',
                       troughcolor='#2d2d44', sliderlength=20)
trackbar_min.set(0)  # Начальное значение Min = 0
trackbar_min.pack()

# --- Слайдер MAX ---
tk.Label(root, text="Max:", fg='#6bffb8', bg='#1a1a2e',
        font=('Arial', 10, 'bold')).pack()
trackbar_max = tk.Scale(root, from_=0, to=100, orient=tk.HORIZONTAL,
                       length=350, bg='#1a1a2e', fg='#6bffb8',
                       troughcolor='#2d2d44', sliderlength=20)
trackbar_max.set(100)  # Начальное значение Max = 100
trackbar_max.pack()

# Функция генерации случайного числа
def generate():
    min_val = int(trackbar_min.get())
    max_val = int(trackbar_max.get())
    # Проверка: Min не должен быть больше Max
    if min_val > max_val:
        messagebox.showerror("Ошибка", "Min должен быть <= Max!")
        return
    # randint - случайное целое число в диапазоне
    progress['value'] = random.randint(min_val, max_val)

# Функция сброса
def reset():
    progress['value'] = 0      # Обнуляем ProgressBar
    trackbar_min.set(0)        # Min = 0
    trackbar_max.set(100)      # Max = 100

# Контейнер для кнопок (чтобы разместить их в ряд)
btn_frame = tk.Frame(root, bg='#1a1a2e')
btn_frame.pack(pady=15)

tk.Button(btn_frame, text="Случайное число", command=generate,
         bg='#b86bff', fg='white', font=('Arial', 10, 'bold'),
         padx=15, pady=8).pack(side=tk.LEFT, padx=10)

tk.Button(btn_frame, text="Сброс", command=reset,
         bg='#ffb86b', fg='white', font=('Arial', 10, 'bold'),
         padx=15, pady=8).pack(side=tk.LEFT, padx=10)

root.mainloop()