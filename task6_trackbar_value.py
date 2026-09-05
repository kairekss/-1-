# -*- coding: utf-8 -*-
"""
ЗАДАНИЕ 7: Вывод значения TrackBar в отдельное окно
"""

import tkinter as tk
# messagebox - для создания всплывающих окон
from tkinter import messagebox

root = tk.Tk()
root.title("Задание 7: Значение TrackBar")
root.geometry("400x250")
root.configure(bg='#1a1a2e')

# Функция показа значения в отдельном окне
def show_value():
    # get() - получаем текущее значение слайдера
    value = trackbar.get()
    # showinfo - показывает информационное окно
    messagebox.showinfo("Значение TrackBar", f"Текущее значение: {value}")

# Создаём слайдер
trackbar = tk.Scale(root, from_=0, to=100, orient=tk.HORIZONTAL,
                   length=300,
                   bg='#1a1a2e', fg='#b86bff',
                   troughcolor='#2d2d44', sliderlength=20)
trackbar.set(50)
trackbar.pack(pady=40)

# Кнопка показывает значение в новом окне
btn = tk.Button(root, text="Показать значение", command=show_value,
               bg='#b86bff', fg='white', font=('Arial', 12, 'bold'),
               padx=20, pady=10)
btn.pack()

root.mainloop()