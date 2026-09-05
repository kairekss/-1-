# -*- coding: utf-8 -*-
"""
ЗАДАНИЕ 6: Вертикальный ProgressBar
"""

import tkinter as tk
from tkinter import ttk

root = tk.Tk()
root.title("Задание 6: Вертикальный ProgressBar")
root.geometry("400x350")
root.configure(bg='#1a1a2e')

# Настраиваем стиль для вертикального ProgressBar
style = ttk.Style()
style.theme_use('clam')
style.configure("Custom.Vertical.TProgressbar", background='#ff6b9d')

# Создаём вертикальный ProgressBar
# orient=tk.VERTICAL - вертикальная ориентация
progress = ttk.Progressbar(root, style="Custom.Vertical.TProgressbar",
                          length=150, mode='determinate', maximum=100,
                          orient=tk.VERTICAL)
progress.pack(pady=20)

def update_progress(value):
    progress['value'] = int(float(value))

# TrackBar управляет вертикальным прогрессом
trackbar = tk.Scale(root, from_=0, to=100, orient=tk.HORIZONTAL,
                   length=300, command=update_progress,
                   bg='#1a1a2e', fg='#ff6b9d',
                   troughcolor='#2d2d44', sliderlength=20)
trackbar.set(50)
trackbar.pack()

root.mainloop()