"""
ОКФРС. ПЗ №1. Доп. задание 2.
По нажатию на кнопку увеличивается размер отображаемого текста
(и уменьшается второй кнопкой).
"""
import tkinter as tk


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


def lerp(c1, c2, t):
    r1, g1, b1 = int(c1[1:3],16), int(c1[3:5],16), int(c1[5:7],16)
    r2, g2, b2 = int(c2[1:3],16), int(c2[3:5],16), int(c2[5:7],16)
    return "#{:02x}{:02x}{:02x}".format(
        int(r1+(r2-r1)*t), int(g1+(g2-g1)*t), int(b1+(b2-b1)*t))


# ---------- КНОПКА ----------
class NeonButton(tk.Canvas):
    def __init__(self, parent, text, command,
                 width=200, height=54, color=ACCENT):
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
    MIN_SIZE = 12
    MAX_SIZE = 96

    def __init__(self, root):
        self.root = root
        root.title("ОКФРС · ПЗ1 · Доп 2 · Изменение размера текста")
        root.geometry("1000x700")
        root.resizable(False, False)

        self.canvas = tk.Canvas(root, width=1000, height=700,
                                highlightthickness=0, bg=BG_TOP)
        self.canvas.pack(fill="both", expand=True)

        for i in range(700):
            self.canvas.create_line(0, i, 1000, i,
                                    fill=lerp(BG_TOP, BG_BOTTOM, i/700))

        # заголовок
        self.canvas.create_text(500, 50,
                                text="ИЗМЕНЕНИЕ РАЗМЕРА ТЕКСТА",
                                fill=TEXT_MAIN,
                                font=("Segoe UI", 22, "bold"))
        self.canvas.create_text(500, 84,
                                text="ОКФРС · ПЗ №1 · Доп 2 · кнопки ±изменяют размер",
                                fill=TEXT_DIM, font=("Segoe UI", 10))
        self.canvas.create_line(250, 108, 750, 108, fill=NEON, width=2)
        self.canvas.create_line(250, 110, 750, 110,
                                fill=lerp(NEON, BG_TOP, 0.7))

        # панель с текстом
        self.canvas.create_rectangle(100, 150, 900, 480,
                                     fill=PANEL_BG, outline=PANEL_BRD)

        # текст, который будем увеличивать
        self.text_id = self.canvas.create_text(
            500, 315,
            text="Привет, Мир!",
            fill=GREEN,
            font=("Segoe UI", 24, "bold"))

        # подпись размера
        self.size_lbl = self.canvas.create_text(
            500, 500,
            text="Размер: 24 pt",
            fill=NEON,
            font=("Consolas", 16, "bold"))

        # кнопки
        btn_minus = NeonButton(root, "−  УМЕНЬШИТЬ",
                               command=self.decrease,
                               width=240, height=54, color=AMBER)
        self.canvas.create_window(290, 560, window=btn_minus)

        btn_plus = NeonButton(root, "+  УВЕЛИЧИТЬ",
                              command=self.increase,
                              width=240, height=54, color=GREEN)
        self.canvas.create_window(710, 560, window=btn_plus)

        btn_reset = NeonButton(root, "↺  СБРОС",
                               command=self.reset,
                               width=200, height=54, color=ACCENT)
        self.canvas.create_window(500, 640, window=btn_reset)

        self.canvas.create_text(500, 685,
                                text="© ОКФРС · ПЗ №1 · Доп 2",
                                fill="#2f3a5a", font=("Segoe UI", 9))

        self.size = 24

    def update_text(self):
        self.canvas.itemconfig(
            self.text_id,
            font=("Segoe UI", self.size, "bold"))
        self.canvas.itemconfig(
            self.size_lbl,
            text=f"Размер: {self.size} pt")

        # при приближении к максимуму — цвет в красный
        if self.size <= 16:
            col = AMBER
        elif self.size <= 40:
            col = GREEN
        elif self.size <= 64:
            col = NEON
        else:
            col = ACCENT
        self.canvas.itemconfig(self.text_id, fill=col)

    def increase(self):
        if self.size < self.MAX_SIZE:
            self.size += 4
            self.update_text()

    def decrease(self):
        if self.size > self.MIN_SIZE:
            self.size -= 4
            self.update_text()

    def reset(self):
        self.size = 24
        self.update_text()


def main():
    root = tk.Tk()
    App(root)
    root.mainloop()


if __name__ == "__main__":
    main()