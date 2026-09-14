"""
ОКФРС. ПЗ №1. Доп. задание 1.
Установить картинку в качестве фона окна (абстрактный фон).

Если рядом с main.py лежит bg.png — используется она.
Если файла нет — рисуется встроенный абстрактный градиент с шумом.
"""
import tkinter as tk
import os
import random
import math


# ---------- ПАЛИТРА ----------
BG_TOP     = "#0a0e1c"
BG_BOTTOM  = "#141a30"
PANEL_BG   = "#0f1425"
PANEL_BRD  = "#2a3150"
NEON       = "#22d3ee"
GREEN      = "#22c55e"
ACCENT     = "#ff4d8d"
AMBER      = "#f4b942"
TEXT_MAIN  = "#eef2ff"
TEXT_DIM   = "#5c6a90"

W, H = 1000, 650
BG_FILE = "bg.png"


def lerp(c1, c2, t):
    r1, g1, b1 = int(c1[1:3],16), int(c1[3:5],16), int(c1[5:7],16)
    r2, g2, b2 = int(c2[1:3],16), int(c2[3:5],16), int(c2[5:7],16)
    return "#{:02x}{:02x}{:02x}".format(
        int(r1+(r2-r1)*t), int(g1+(g2-g1)*t), int(b1+(b2-b1)*t))


# ---------- АБСТРАКТНЫЙ ФОН (если картинки нет) ----------
def draw_abstract_background(canvas):
    """Рисует абстрактный фон с градиентом, кругами и линиями."""
    # 1. вертикальный градиент
    for i in range(H):
        canvas.create_line(0, i, W, i,
                           fill=lerp(BG_TOP, BG_BOTTOM, i/H))
    # 2. большие размытые пятна
    blobs = [
        (150, 180, 260, "#1a3d5c"),
        (820, 480, 320, "#3d1a3d"),
        (500, 300, 380, "#0f2a4a"),
        (300, 550, 220, "#2a1a3d"),
        (750, 150, 240, "#1a2a4a"),
    ]
    for cx, cy, r, color in blobs:
        # 3 круга = «мягкое пятно»
        for k in range(3, 0, -1):
            rr = r * k / 3
            c = lerp(color, BG_TOP, 0.15 * (3 - k))
            canvas.create_oval(cx-rr, cy-rr, cx+rr, cy+rr,
                               fill=c, outline="")
    # 3. тонкие неоновые линии
    for _ in range(8):
        x1 = random.randint(0, W)
        y1 = random.randint(0, H)
        x2 = x1 + random.randint(-200, 200)
        y2 = y1 + random.randint(-200, 200)
        canvas.create_line(x1, y1, x2, y2,
                           fill=lerp(NEON, BG_TOP, 0.75), width=1)
    # 4. шум — звёздочки
    for _ in range(180):
        x = random.randint(0, W)
        y = random.randint(0, H)
        r = random.choice([0.6, 0.8, 1.0, 1.4])
        canvas.create_oval(x-r, y-r, x+r, y+r,
                           fill="#ffffff", outline="")


# ---------- КНОПКА ----------
class NeonButton(tk.Canvas):
    def __init__(self, parent, text, command,
                 width=240, height=54, color=ACCENT):
        super().__init__(parent, width=width, height=height,
                         bg=PANEL_BG, highlightthickness=0)
        self.command = command
        self.text = text
        self.color = color
        self.w, self.h = width, height
        self.hovered = False
        self.pressed = False
        self._draw()
        self.bind("<Enter>", self._enter)
        self.bind("<Leave>", self._leave)
        self.bind("<ButtonPress>", self._press)
        self.bind("<ButtonRelease>", self._release)

    def _draw(self):
        self.delete("all")
        c = self.color
        if self.pressed:
            c = lerp(self.color, "#000000", 0.3)
        elif self.hovered:
            c = lerp(self.color, "#ffffff", 0.2)
        if self.hovered:
            for i in range(4, 0, -1):
                self.create_rectangle(-i, -i, self.w+i, self.h+i,
                                      outline=lerp(self.color, PANEL_BG, i*0.2))
        self.create_rectangle(4, 5, self.w+4, self.h+5,
                              fill="#02040a", outline="")
        self.create_rectangle(0, 0, self.w, self.h, fill=c,
                              outline=lerp(c, "#ffffff", 0.4))
        self.create_rectangle(2, 2, self.w-2, self.h//2,
                              fill=lerp(c, "#ffffff", 0.25), outline="")
        self.create_text(self.w/2, self.h/2, text=self.text,
                         fill="#ffffff", font=("Segoe UI", 12, "bold"))

    def _enter(self, e):
        self.hovered = True; self.configure(cursor="hand2"); self._draw()

    def _leave(self, e):
        self.hovered = False; self.pressed = False
        self.configure(cursor=""); self._draw()

    def _press(self, e):
        self.pressed = True; self._draw()

    def _release(self, e):
        self.pressed = False; self._draw()
        if callable(self.command):
            self.command()


# ---------- ГЛАВНОЕ ОКНО ----------
class App:
    def __init__(self, root):
        self.root = root
        root.title("ОКФРС · ПЗ1 · Доп 1 · Картинка-фон")
        root.geometry(f"{W}x{H}")
        root.resizable(False, False)

        self.canvas = tk.Canvas(root, width=W, height=H,
                                highlightthickness=0, bg=BG_TOP)
        self.canvas.pack(fill="both", expand=True)

        # фон: картинка или абстрактный
        self.bg_photo = None
        if os.path.exists(BG_FILE):
            try:
                self.bg_photo = tk.PhotoImage(file=BG_FILE)
                # если картинка не 1000x650 — просто кладём как есть
                self.canvas.create_image(0, 0, image=self.bg_photo,
                                         anchor="nw", tags="bg")
                self.status_text = f"✔ Фон: загружена картинка «{BG_FILE}»"
            except Exception as e:
                draw_abstract_background(self.canvas)
                self.status_text = f"⚠ Ошибка загрузки: {e}. Использован встроенный фон."
        else:
            draw_abstract_background(self.canvas)
            self.status_text = "ℹ bg.png не найдена — использован встроенный абстрактный фон."

        # полупрозрачная тёмная «шапка» для читаемости текста
        self.canvas.create_rectangle(0, 0, W, 130,
                                     fill="#000000", outline="",
                                     stipple="gray50")
        self.canvas.create_rectangle(0, H-140, W, H,
                                     fill="#000000", outline="",
                                     stipple="gray50")

        # заголовок
        self.canvas.create_text(W//2, 50,
                                text="АБСТРАКТНЫЙ ФОН ОКНА",
                                fill=TEXT_MAIN,
                                font=("Segoe UI", 24, "bold"))
        self.canvas.create_text(W//2, 88,
                                text="ОКФРС · ПЗ №1 · Доп 1 · картинка в качестве фона",
                                fill=TEXT_DIM, font=("Segoe UI", 10))
        self.canvas.create_line(W//2-300, 112, W//2+300, 112,
                                fill=NEON, width=2)

        # статус
        self.canvas.create_text(W//2, H-100,
                                text=self.status_text,
                                fill=GREEN, font=("Segoe UI", 11))

        # кнопка «показать/скрыть подсказку»
        btn = NeonButton(root, "ℹ  ЧТО ЭТО?",
                         command=self.show_info,
                         width=240, height=54, color=NEON)
        self.canvas.create_window(W//2, H-50, window=btn)

    def show_info(self):
        from tkinter import messagebox
        messagebox.showinfo(
            "Доп 1 · Картинка-фон",
            "В этом задании требовалось установить картинку\n"
            "в качестве фона окна (не котики, абстрактный фон).\n\n"
            "Как использовать свою картинку:\n"
            "1. Положи файл bg.png рядом с main.py.\n"
            "2. Размер картинки лучше сделать 1000x650.\n"
            "3. Запусти программу заново — она подхватит твой фон.\n\n"
            "Если файла нет — программа сама рисует\n"
            "абстрактный градиент с пятнами и звёздочками."
        )


def main():
    root = tk.Tk()
    App(root)
    root.mainloop()


if __name__ == "__main__":
    main()