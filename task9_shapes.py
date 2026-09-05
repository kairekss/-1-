# -*- coding: utf-8 -*-
"""
ДОПОЛНИТЕЛЬНЫЕ ЗАДАНИЯ: Фигуры
"""

import tkinter as tk

root = tk.Tk()
root.title("Дополнительные задания: Фигуры")
root.geometry("550x600")
root.configure(bg='#1a1a2e')

# Canvas - полотно для рисования
canvas = tk.Canvas(root, width=450, height=200, bg='#16213e',
                   highlightthickness=2, highlightcolor='#00d4ff')
canvas.pack(pady=10)


# Функция перерисовки фигур
def update_shapes(value=None):
    # Удаляем всё с Canvas
    canvas.delete("all")

    # Получаем значения со слайдеров
    radius = int(trackbar_radius.get())
    count = int(trackbar_count.get())
    rect_w = int(trackbar_rect_w.get())
    rect_h = int(trackbar_rect_h.get())

    # Центр Canvas (x, y)
    cx, cy = 225, 100

    # --- Рисуем круги (пиковый индикатор) ---
    spacing = 35  # Расстояние между кругами
    total_width = (count - 1) * spacing  # Общая ширина всех кругов
    start_x = cx - total_width // 2  # Начальная позиция X

    for i in range(count):
        x = start_x + i * spacing  # Текущая позиция X
        height_ratio = (i + 1) / count  # Отношение высоты (0.2, 0.4, 0.6, ...)
        r = int(radius * (0.5 + 0.5 * height_ratio))  # Радиус круга
        y_offset = int(r * 0.7)  # Смещение по Y

        # Цвет от зелёного к красному
        green = int(255 * (1 - height_ratio * 0.8))
        red = int(255 * height_ratio * 0.8)
        color = f'#{red:02x}{green:02x}00'

        # create_oval(x1, y1, x2, y2, fill, outline) - рисует круг
        canvas.create_oval(x - r, cy - y_offset - r,
                           x + r, cy - y_offset + r,
                           fill=color, outline='#00d4ff', width=2)

    # --- Рисуем прямоугольник ---
    # create_rectangle(x1, y1, x2, y2, fill, outline)
    canvas.create_rectangle(cx + 160 - rect_w // 2, cy - rect_h // 2,
                            cx + 160 + rect_w // 2, cy + rect_h // 2,
                            fill='#3498db', outline='#00d4ff', width=2)

    # --- Выводим информацию ---
    info = f"Круги: {count} | Радиус: {radius} | Прям.: {rect_w}x{rect_h}"
    canvas.create_text(cx, 190, text=info, fill='#8888aa', font=('Arial', 10))


# --- Слайдер радиуса круга ---
tk.Label(root, text="Радиус круга:", fg='#ff6b9d', bg='#1a1a2e').pack()
trackbar_radius = tk.Scale(root, from_=10, to=80, orient=tk.HORIZONTAL,
                           length=400, command=update_shapes,
                           bg='#1a1a2e', fg='#ff6b9d',
                           troughcolor='#2d2d44', sliderlength=20)
trackbar_radius.set(40)
trackbar_radius.pack()

# --- Слайдер количества кругов ---
tk.Label(root, text="Количество кругов:", fg='#6bcbff', bg='#1a1a2e').pack()
trackbar_count = tk.Scale(root, from_=1, to=8, orient=tk.HORIZONTAL,
                          length=400, command=update_shapes,
                          bg='#1a1a2e', fg='#6bcbff',
                          troughcolor='#2d2d44', sliderlength=20)
trackbar_count.set(3)
trackbar_count.pack()

# --- Слайдер ширины прямоугольника ---
tk.Label(root, text="Ширина прямоугольника:", fg='#ffb86b', bg='#1a1a2e').pack()
trackbar_rect_w = tk.Scale(root, from_=20, to=150, orient=tk.HORIZONTAL,
                           length=400, command=update_shapes,
                           bg='#1a1a2e', fg='#ffb86b',
                           troughcolor='#2d2d44', sliderlength=20)
trackbar_rect_w.set(80)
trackbar_rect_w.pack()

# --- Слайдер высоты прямоугольника ---
tk.Label(root, text="Высота прямоугольника:", fg='#6bffb8', bg='#1a1a2e').pack()
trackbar_rect_h = tk.Scale(root, from_=20, to=150, orient=tk.HORIZONTAL,
                           length=400, command=update_shapes,
                           bg='#1a1a2e', fg='#6bffb8',
                           troughcolor='#2d2d44', sliderlength=20)
trackbar_rect_h.set(60)
trackbar_rect_h.pack()

# Инициализация фигур при старте
update_shapes()
root.mainloop()