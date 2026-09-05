# -*- coding: utf-8 -*-
"""
ЗАДАНИЕ 3: Кнопка увеличивает счётчик на 1
"""

import tkinter as tk

root = tk.Tk()
root.title("Задание 3: Счётчик")
root.geometry("350x250")
root.configure(bg='#1a1a2e')

# Переменная для хранения значения счётчика
counter = 0

# Создаём метку для отображения счётчика
# font - большой шрифт, fg - красный цвет
label = tk.Label(root, text="0", font=('Arial', 48, 'bold'),
                fg='#ff6b6b', bg='#1a1a2e')
label.pack(pady=30)

# Функция увеличения счётчика
def increment():
    global counter  # Говорим, что используем глобальную переменную
    counter += 1    # Увеличиваем на 1
    label.config(text=str(counter))  # Обновляем текст метки

# Создаём кнопку, которая вызывает функцию increment
btn = tk.Button(root, text="Увеличить на 1", command=increment,
               bg='#ff6b6b', fg='white', font=('Arial', 14, 'bold'),
               padx=30, pady=10)
btn.pack()

root.mainloop()