# -*- coding: utf-8 -*-
"""
Задание 1: Кнопка выводит "Привет, Мир" на Label
"""

import tkinter as tk

root = tk.Tk()
root.title("Задание 1: Label")
root.geometry("300x200")
root.configure(bg='#1a1a2e')

label = tk.Label(root, text="", font=('Arial', 18, 'bold'),
                fg='#00d4ff', bg='#1a1a2e')
label.pack(pady=40)

btn = tk.Button(root, text="Показать приветствие",
               command=lambda: label.config(text="Привет, Мир"),
               bg='#00d4ff', fg='white', font=('Arial', 12, 'bold'),
               padx=20, pady=10)
btn.pack()

root.mainloop()