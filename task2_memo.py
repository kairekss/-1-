# -*- coding: utf-8 -*-
"""
Задание 2: Кнопка выводит "Привет, Мир" в поле Memo (Text)
"""

import tkinter as tk

root = tk.Tk()
root.title("Задание 2: Memo")
root.geometry("400x300")
root.configure(bg='#1a1a2e')

memo = tk.Text(root, height=5, width=40, font=('Consolas', 12),
              bg='#16213e', fg='#e0e0e0', insertbackground='#00d4ff')
memo.pack(pady=20)

btn = tk.Button(root, text="Показать в Memo",
               command=lambda: memo.insert(tk.END, "Привет, Мир\n"),
               bg='#00d4ff', fg='white', font=('Arial', 12, 'bold'),
               padx=20, pady=10)
btn.pack()

root.mainloop()