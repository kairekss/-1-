"""
ОКФРС. ПЗ №1. Задание 6.
Вертикальный ProgressBar — отображение уровня (громкость).
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
                 width=200, height=50, color=ACCENT):
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
                         fill="#ffffff", font=("Segoe UI", 11, "bold"))

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


# ---------- ВЕРТИКАЛЬНЫЙ PROGRESSBAR ----------
class VerticalProgressBar(tk.Canvas):
    """Вертикальный прогресс-бар в стиле «колонка с уровнями»."""
    def __init__(self, parent, width=90, height=340):
        super().__init__(parent, width=width, height=height,
                         bg=PANEL_BG, highlightthickness=0)
        self.w, self.h = width, height
        self.value = 0  # 0..100
        self._draw()

    def set_value(self, val):
        self.value = max(0, min(100, val))
        self._draw()

    def _draw(self):
        self.delete("all")

        # фон колонки
        self.create_rectangle(0, 0, self.w, self.h,
                              fill="#060a16", outline=PANEL_BRD)

        # заполнение снизу вверх
        fill_h = int(self.h * self.value / 100)
        if fill_h > 0:
            if self.value < 30:
                col = GREEN
            elif self.value < 70:
                col = NEON
            elif self.value < 90:
                col = AMBER
            else:
                col = ACCENT

            y_top = self.h - fill_h
            # градиент по высоте
            steps = max(fill_h // 4, 1)
            for i in range(steps):
                t = i / steps
                y1 = y_top + int(i * fill_h / steps)
                y2 = y_top + int((i + 1) * fill_h / steps)
                c = lerp(col, lerp(col, "#ffffff", 0.3), t)
                self.create_rectangle(3, y1, self.w - 3, y2,
                                      fill=c, outline="")

            # блик слева
            self.create_rectangle(3, y_top, self.w // 2, self.h - 3,
                                  fill=lerp(col, "#ffffff", 0.3), outline="")

        # риски уровня — каждые 10%
        for i in range(11):
            y = self.h - int(self.h * i / 10)
            self.create_line(self.w - 15, y, self.w - 3, y,
                             fill="#3a4363")

        # рамка
        self.create_rectangle(0, 0, self.w - 1, self.h - 1,
                              outline=PANEL_BRD, width=1)

        # текст с процентом
        text_col = "#ffffff" if self.value > 15 else TEXT_DIM
        self.create_text(self.w // 2, self.h // 2,
                         text=f"{self.value}%",
                         fill=text_col,
                         font=("Consolas", 13, "bold"))


# ---------- ГЛАВНОЕ ОКНО ----------
class App:
    def __init__(self, root):
        self.root = root
        root.title("ОКФРС · ПЗ1 · Задание 6 · Вертикальный ProgressBar")
        root.geometry("1000x650")
        root.resizable(False, False)

        self.canvas = tk.Canvas(root, width=1000, height=650,
                                highlightthickness=0, bg=BG_TOP)
        self.canvas.pack(fill="both", expand=True)

        for i in range(650):
            self.canvas.create_line(0, i, 1000, i,
                                    fill=lerp(BG_TOP, BG_BOTTOM, i/650))

        # заголовок
        self.canvas.create_text(500, 50,
                                text="ВЕРТИКАЛЬНЫЙ PROGRESSBAR",
                                fill=TEXT_MAIN,
                                font=("Segoe UI", 22, "bold"))
        self.canvas.create_text(500, 84,
                                text="ОКФРС · ПЗ №1 · Задание 6 · уровень громкости",
                                fill=TEXT_DIM, font=("Segoe UI", 10))
        self.canvas.create_line(250, 108, 750, 108, fill=NEON, width=2)
        self.canvas.create_line(250, 110, 750, 110,
                                fill=lerp(NEON, BG_TOP, 0.7))

        # ---- Колонка сбоку ----
        self.canvas.create_text(170, 140,
                                text="▸ УРОВЕНЬ",
                                fill=NEON,
                                font=("Segoe UI", 10, "bold"), anchor="w")

        self.canvas.create_rectangle(155, 165, 250, 515,
                                     fill=PANEL_BG, outline=PANEL_BRD)

        self.vbar = VerticalProgressBar(root, width=80, height=336)
        self.canvas.create_window(162, 172, window=self.vbar, anchor="nw")

        # ---- Панель управления справа ----
        self.canvas.create_rectangle(320, 160, 850, 500,
                                     fill=PANEL_BG, outline=PANEL_BRD)

        self.canvas.create_text(340, 190,
                                text="▸ TRACKBAR (громкость)",
                                fill=NEON,
                                font=("Segoe UI", 10, "bold"), anchor="w")

        self.scale = tk.Scale(root, from_=0, to=100, orient="horizontal",
                              bg=PANEL_BG, fg=TEXT_MAIN,
                              troughcolor="#060a16",
                              highlightthickness=0, bd=0,
                              length=480, activebackground=ACCENT,
                              font=("Segoe UI", 10),
                              command=self.on_scale)
        self.scale.set(0)
        self.canvas.create_window(340, 210,
                                  window=self.scale, anchor="nw")

        # Большая цифра
        self.canvas.create_text(600, 300,
                                text="▸ ЗНАЧЕНИЕ",
                                fill=TEXT_DIM,
                                font=("Segoe UI", 10, "bold"))
        self.value_lbl = self.canvas.create_text(
            600, 370, text="0 %",
            fill=GREEN, font=("Consolas", 60, "bold"))

        # Быстрые кнопки 25 / 50 / 75 / 100
        labels = [("25%", 25, GREEN), ("50%", 50, NEON),
                  ("75%", 75, AMBER), ("100%", 100, ACCENT)]
        x_start = 420
        for i, (label, val, col) in enumerate(labels):
            btn = NeonButton(root, label,
                             command=lambda v=val: self.set_value(v),
                             width=100, height=46, color=col)
            self.canvas.create_window(x_start + i*110, 440,
                                      window=btn)

        self.canvas.create_text(500, 600,
                                text="© ОКФРС · ПЗ №1 · Задание 6",
                                fill="#2f3a5a", font=("Segoe UI", 9))

    def on_scale(self, val):
        v = int(float(val))
        self.vbar.set_value(v)
        if v < 30:
            col = GREEN
        elif v < 70:
            col = NEON
        elif v < 90:
            col = AMBER
        else:
            col = ACCENT
        self.canvas.itemconfig(self.value_lbl,
                               text=f"{v} %", fill=col)

    def set_value(self, v):
        self.scale.set(v)
        self.on_scale(v)


def main():
    root = tk.Tk()
    App(root)
    root.mainloop()


if __name__ == "__main__":
    main()