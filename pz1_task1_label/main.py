"""
ОКФРС. ПЗ №1. Задание 1.
Кнопка -> по нажатию в Label выводится «Привет, Мир».
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
TEXT_MAIN  = "#eef2ff"
TEXT_DIM   = "#5c6a90"


def lerp(c1, c2, t):
    r1, g1, b1 = int(c1[1:3],16), int(c1[3:5],16), int(c1[5:7],16)
    r2, g2, b2 = int(c2[1:3],16), int(c2[3:5],16), int(c2[5:7],16)
    return "#{:02x}{:02x}{:02x}".format(
        int(r1+(r2-r1)*t), int(g1+(g2-g1)*t), int(b1+(b2-b1)*t))


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


class App:
    def __init__(self, root):
        self.root = root
        root.title("ОКФРС · ПЗ1 · Задание 1 · Привет, Мир в Label")
        root.geometry("900x560")
        root.resizable(False, False)

        self.canvas = tk.Canvas(root, width=900, height=560,
                                highlightthickness=0, bg=BG_TOP)
        self.canvas.pack(fill="both", expand=True)

        # градиентный фон
        for i in range(560):
            self.canvas.create_line(0, i, 900, i,
                                    fill=lerp(BG_TOP, BG_BOTTOM, i/560))

        # заголовок
        self.canvas.create_text(450, 50,
                                text="КНОПКА + LABEL",
                                fill=TEXT_MAIN,
                                font=("Segoe UI", 22, "bold"))
        self.canvas.create_text(450, 84,
                                text="ОКФРС · ПЗ №1 · Задание 1 · «Привет, Мир»",
                                fill=TEXT_DIM, font=("Segoe UI", 10))
        self.canvas.create_line(250, 108, 650, 108, fill=NEON, width=2)
        self.canvas.create_line(250, 110, 650, 110,
                                fill=lerp(NEON, BG_TOP, 0.7))

        # панель (аналог Label)
        self.canvas.create_rectangle(150, 200, 750, 330,
                                     fill=PANEL_BG, outline=PANEL_BRD)
        self.canvas.create_text(450, 220,
                                text="▸ LABEL",
                                fill=NEON,
                                font=("Segoe UI", 10, "bold"))

        # текст внутри Label
        self.label_text = self.canvas.create_text(
            450, 275, text="— здесь появится текст —",
            fill=TEXT_DIM, font=("Segoe UI", 20, "bold"))

        # кнопка
        btn = NeonButton(root, "НАЖАТЬ", command=self.on_click,
                         width=260, height=56, color=ACCENT)
        self.canvas.create_window(450, 420, window=btn)

        self.canvas.create_text(450, 500,
                                text="© ОКФРС · ПЗ №1 · Задание 1",
                                fill="#2f3a5a", font=("Segoe UI", 9))

    def on_click(self):
        self.canvas.itemconfig(self.label_text,
                               text="Привет, Мир!",
                               fill=GREEN)


def main():
    root = tk.Tk()
    App(root)
    root.mainloop()


if __name__ == "__main__":
    main()