"""
ОКФРС. ПЗ №1. Задание 3.
Кнопка -> по каждому нажатию значение в окошке увеличивается на единицу.
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


class NeonButton(tk.Canvas):
    def __init__(self, parent, text, command,
                 width=280, height=56, color=ACCENT):
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


class App:
    def __init__(self, root):
        self.root = root
        root.title("ОКФРС · ПЗ1 · Задание 3 · Счётчик нажатий")
        root.geometry("900x600")
        root.resizable(False, False)

        self.canvas = tk.Canvas(root, width=900, height=600,
                                highlightthickness=0, bg=BG_TOP)
        self.canvas.pack(fill="both", expand=True)

        for i in range(600):
            self.canvas.create_line(0, i, 900, i,
                                    fill=lerp(BG_TOP, BG_BOTTOM, i/600))

        # заголовок
        self.canvas.create_text(450, 50,
                                text="СЧЁТЧИК НАЖАТИЙ",
                                fill=TEXT_MAIN,
                                font=("Segoe UI", 22, "bold"))
        self.canvas.create_text(450, 84,
                                text="ОКФРС · ПЗ №1 · Задание 3 · +1 при каждом клике",
                                fill=TEXT_DIM, font=("Segoe UI", 10))
        self.canvas.create_line(250, 108, 650, 108, fill=NEON, width=2)
        self.canvas.create_line(250, 110, 650, 110,
                                fill=lerp(NEON, BG_TOP, 0.7))

        # панель со значением
        self.canvas.create_rectangle(250, 160, 650, 360,
                                     fill=PANEL_BG, outline=PANEL_BRD)
        self.canvas.create_text(450, 190,
                                text="▸ ЗНАЧЕНИЕ",
                                fill=NEON,
                                font=("Segoe UI", 10, "bold"))

        # большая цифра счётчика
        self.counter_lbl = self.canvas.create_text(
            450, 275, text="0",
            fill=GREEN, font=("Consolas", 72, "bold"))

        # кнопки
        btn_inc = NeonButton(root, "+1   НАЖАТЬ",
                             command=self.on_click,
                             width=280, height=56, color=ACCENT)
        self.canvas.create_window(310, 440, window=btn_inc)

        btn_reset = NeonButton(root, "СБРОСИТЬ",
                               command=self.on_reset,
                               width=200, height=56, color=AMBER)
        self.canvas.create_window(650, 440, window=btn_reset)

        self.canvas.create_text(450, 550,
                                text="© ОКФРС · ПЗ №1 · Задание 3",
                                fill="#2f3a5a", font=("Segoe UI", 9))

        self.count = 0

    def on_click(self):
        self.count += 1
        # меняем цвет в зависимости от значения
        if self.count < 10:
            color = GREEN
        elif self.count < 30:
            color = NEON
        elif self.count < 60:
            color = AMBER
        else:
            color = ACCENT
        self.canvas.itemconfig(self.counter_lbl,
                               text=str(self.count),
                               fill=color)

    def on_reset(self):
        self.count = 0
        self.canvas.itemconfig(self.counter_lbl,
                               text="0", fill=GREEN)


def main():
    root = tk.Tk()
    App(root)
    root.mainloop()


if __name__ == "__main__":
    main()