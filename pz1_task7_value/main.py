"""
ОКФРС. ПЗ №1. Задание 7.
Вывод в отдельное окно значения TrackBar.
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


# ---------- ОТДЕЛЬНОЕ ОКНО ЗНАЧЕНИЯ ----------
class ValueWindow:
    """Всплывающее окно с крупным значением TrackBar."""
    def __init__(self, parent):
        self.parent = parent
        self.win = tk.Toplevel(parent)
        self.win.title("Значение TrackBar")
        self.win.geometry("420x300")
        self.win.resizable(False, False)
        self.win.configure(bg=BG_TOP)
        # окно поверх родительского
        self.win.transient(parent)

        self.canvas = tk.Canvas(self.win, width=420, height=300,
                                highlightthickness=0, bg=BG_TOP)
        self.canvas.pack(fill="both", expand=True)

        for i in range(300):
            self.canvas.create_line(0, i, 420, i,
                                    fill=lerp(BG_TOP, BG_BOTTOM, i/300))

        self.canvas.create_text(210, 40,
                                text="ЗНАЧЕНИЕ TRACKBAR",
                                fill=TEXT_MAIN,
                                font=("Segoe UI", 14, "bold"))
        self.canvas.create_line(80, 65, 340, 65, fill=NEON, width=2)

        self.value_lbl = self.canvas.create_text(
            210, 150, text="0",
            fill=GREEN, font=("Consolas", 80, "bold"))

        self.canvas.create_text(210, 250,
                                text="обновляется в реальном времени",
                                fill=TEXT_DIM,
                                font=("Segoe UI", 10))

    def set_value(self, v):
        self.canvas.itemconfig(self.value_lbl, text=str(v))
        if v < 30:
            col = GREEN
        elif v < 70:
            col = NEON
        elif v < 90:
            col = AMBER
        else:
            col = ACCENT
        self.canvas.itemconfig(self.value_lbl, fill=col)


# ---------- ГЛАВНОЕ ОКНО ----------
class App:
    def __init__(self, root):
        self.root = root
        root.title("ОКФРС · ПЗ1 · Задание 7 · Отдельное окно значения")
        root.geometry("1000x600")
        root.resizable(False, False)

        self.canvas = tk.Canvas(root, width=1000, height=600,
                                highlightthickness=0, bg=BG_TOP)
        self.canvas.pack(fill="both", expand=True)

        for i in range(600):
            self.canvas.create_line(0, i, 1000, i,
                                    fill=lerp(BG_TOP, BG_BOTTOM, i/600))

        # заголовок
        self.canvas.create_text(500, 50,
                                text="ОТДЕЛЬНОЕ ОКНО СО ЗНАЧЕНИЕМ",
                                fill=TEXT_MAIN,
                                font=("Segoe UI", 22, "bold"))
        self.canvas.create_text(500, 84,
                                text="ОКФРС · ПЗ №1 · Задание 7 · вывод значения TrackBar",
                                fill=TEXT_DIM, font=("Segoe UI", 10))
        self.canvas.create_line(250, 108, 750, 108, fill=NEON, width=2)
        self.canvas.create_line(250, 110, 750, 110,
                                fill=lerp(NEON, BG_TOP, 0.7))

        # TrackBar
        self.canvas.create_text(150, 160,
                                text="▸ TRACKBAR",
                                fill=NEON,
                                font=("Segoe UI", 10, "bold"), anchor="w")

        self.scale = tk.Scale(root, from_=0, to=100, orient="horizontal",
                              bg=PANEL_BG, fg=TEXT_MAIN,
                              troughcolor="#060a16",
                              highlightthickness=0, bd=0,
                              length=700, activebackground=ACCENT,
                              font=("Segoe UI", 10),
                              command=self.on_scale)
        self.scale.set(0)
        self.canvas.create_window(150, 180,
                                  window=self.scale, anchor="nw")

        # Большая цифра на главном окне
        self.canvas.create_text(500, 290,
                                text="▸ ЗНАЧЕНИЕ (в главном окне)",
                                fill=TEXT_DIM,
                                font=("Segoe UI", 10, "bold"))
        self.value_main = self.canvas.create_text(
            500, 380, text="0",
            fill=GREEN, font=("Consolas", 72, "bold"))

        # Кнопки
        btn_open = NeonButton(root, "◱  ОТКРЫТЬ ОКНО ЗНАЧЕНИЯ",
                              command=self.open_window,
                              width=340, height=54, color=ACCENT)
        self.canvas.create_window(500, 500, window=btn_open)

        self.canvas.create_text(500, 570,
                                text="© ОКФРС · ПЗ №1 · Задание 7",
                                fill="#2f3a5a", font=("Segoe UI", 9))

        # всплывающее окно пока не создано
        self.value_win = None

    def on_scale(self, val):
        v = int(float(val))

        # главное окно
        if v < 30:
            col = GREEN
        elif v < 70:
            col = NEON
        elif v < 90:
            col = AMBER
        else:
            col = ACCENT
        self.canvas.itemconfig(self.value_main, text=str(v), fill=col)

        # если окно открыто — обновляем и там
        if self.value_win is not None:
            try:
                self.value_win.set_value(v)
            except tk.TclError:
                self.value_win = None

    def open_window(self):
        # создаём один раз
        if self.value_win is None:
            self.value_win = ValueWindow(self.root)
        # иначе поднять наверх
        else:
            self.value_win.win.deiconify()
            self.value_win.win.lift()
        # синхронизация текущего значения
        self.value_win.set_value(int(float(self.scale.get())))


def main():
    root = tk.Tk()
    App(root)
    root.mainloop()


if __name__ == "__main__":
    main()