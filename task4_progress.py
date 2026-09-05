# -*- coding: utf-8 -*-
"""
ЗАДАНИЕ 4-5: TrackBar управляет ProgressBar
"""

# Импортируем tkinter и ttk (для стилизованных виджетов)
import tkinter as tk
from tkinter import ttk

root = tk.Tk()
root.title("Задание 4-5: TrackBar → ProgressBar")
root.geometry("400x300")
root.configure(bg='#1a1a2e')

# Настраиваем стиль для ProgressBar
style = ttk.Style()
style.theme_use('clam')  # Используем тему 'clam'
# Настраиваем цвет полоски прогресса
style.configure("Custom.Horizontal.TProgressbar", background='#00d4ff')

# Создаём ProgressBar (индикатор прогресса)
# length - длина в пикселях, mode - режим (determinate - фиксированный)
# maximum - максимальное значение (100)
progress = ttk.Progressbar(root, style="Custom.Horizontal.TProgressbar",
                          length=300, mode='determinate', maximum=100)
progress.pack(pady=30)

# Функция обновления прогресса при движении слайдера
def update_progress(value):
    # value - значение от слайдера (строка), преобразуем в число
    progress['value'] = int(float(value))

# Создаём слайдер (TrackBar)
# from_ - минимальное значение, to - максимальное
# orient - ориентация (горизонтальная)
# command - функция, вызываемая при изменении
trackbar = tk.Scale(root, from_=0, to=100, orient=tk.HORIZONTAL,
                   length=300, command=update_progress,
                   bg='#1a1a2e', fg='#00d4ff',
                   troughcolor='#2d2d44', sliderlength=20)
# Устанавливаем начальное значение 50
trackbar.set(50)
trackbar.pack()

root.mainloop()