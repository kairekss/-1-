"""
ОКФРС. ПЗ №1. Задание 5.
Компонентом TrackBar задавать значение ProgressBar.
Плюс кнопка «АВТО» — плавно меняет значение.
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

    def set_text(self, t):
        self.text = t
        self._draw()

    def set_color(self, c):
        self.color = c
        self._draw()

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


# ---------- PROGRESSBAR ----------
class ProgressBar(tk.Canvas):
    def __init__(self, parent, width=680, height=44):
        super().__init__(parent, width=width, height=height,
                         bg=PANEL_BG, highlightthickness=0)
        self.w, self.h = width, height
        self.value = 0
        self._draw()

    def set_value(self, val):
        self.value = max(0, min(100, val))
        self._draw()

    def _draw(self):
        self.delete("all")
        # фон
        self.create_rectangle(0, 0, self.w, self.h,
                              fill="#060a16", outline=PANEL_BRD)

        # заполнение
        fill_w = int(self.w * self.value / 100)
        if fill_w > 0:
            if self.value < 30:
                col = GREEN
            elif self.value < 70:
                col = NEON
            elif self.value < 90:
                col = AMBER
            else:
                col = ACCENT

            steps = max(fill_w // 4, 1)
            for i in range(steps):
                t = i / steps
                x1 = int(i * fill_w / steps)
                x2 = int((i + 1) * fill_w / steps)
                c = lerp(col, lerp(col, "#ffffff", 0.3), t)
                self.create_rectangle(x1, 2, x2, self.h - 2,
                                      fill=c, outline="")
            # блик
            self.create_rectangle(0, 2, fill_w, self.h // 2,
                                  fill=lerp(col, "#ffffff", 0.25), outline="")

        # рамка
        self.create_rectangle(0, 0, self.w - 1, self.h - 1,
                              outline=PANEL_BRD, width=1)

        # процент внутри
        if self.value > 12:
            self.create_text(
                8, self.h // 2,
                text=f"{self.value}%",
                fill="#ffffff", anchor="w",
                font=("Consolas", 12, "bold"))


# ---------- ГЛАВНОЕ ОКНО ----------
class App:
    def __init__(self, root):
        self.root = root
        root.title("ОКФРС · ПЗ1 · Задание 5 · TrackBar -> ProgressBar")
        root.geometry("1000x620")
        root.resizable(False, False)

        self.canvas = tk.Canvas(root, width=1000, height=620,
                                highlightthickness=0, bg=BG_TOP)
        self.canvas.pack(fill="both", expand=True)

        for i in range(620):
            self.canvas.create_line(0, i, 1000, i,
                                    fill=lerp(BG_TOP, BG_BOTTOM, i/620))

        # заголовок
        self.canvas.create_text(500, 50,
                                text="TRACKBAR → PROGRESSBAR",
                                fill=TEXT_MAIN,
                                font=("Segoe UI", 22, "bold"))
        self.canvas.create_text(500, 84,
                                text="ОКФРС · ПЗ №1 · Задание 5 · связка ползунок → прогресс",
                                fill=TEXT_DIM, font=("Segoe UI", 10))
        self.canvas.create_line(250, 108, 750, 108, fill=NEON, width=2)
        self.canvas.create_line(250, 110, 750, 110,
                                fill=lerp(NEON, BG_TOP, 0.7))

        # TrackBar
        self.canvas.create_text(150, 140,
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
        self.canvas.create_window(150, 160, window=self.scale, anchor="nw")

        # ProgressBar
        self.canvas.create_text(150, 250,
                                text="▸ PROGRESSBAR",
                                fill=NEON,
                                font=("Segoe UI", 10, "bold"), anchor="w")

        self.canvas.create_rectangle(150, 275, 850, 330,
                                     fill=PANEL_BG, outline=PANEL_BRD)
        self.progress = ProgressBar(root, width=680, height=44)
        self.canvas.create_window(160, 282,
                                  window=self.progress, anchor="nw")

        # Большая цифра
        self.value_lbl = self.canvas.create_text(
            500, 420, text="0 %",
            fill=GREEN, font=("Consolas", 64, "bold"))

        # Кнопки
        self.btn_auto = NeonButton(root, "▶  АВТО",
                                   command=self.toggle_auto,
                                   width=200, height=54, color=GREEN)
        self.canvas.create_window(300, 520, window=self.btn_auto)

        self.btn_reset = NeonButton(root, "↺  СБРОС",
                                    command=self.reset,
                                    width=200, height=54, color=AMBER)
        self.canvas.create_window(520, 520, window=self.btn_reset)

        self.canvas.create_text(500, 590,
                                text="© ОКФРС · ПЗ №1 · Задание 5",
                                fill="#2f3a5a", font=("Segoe UI", 9))

        self.auto_running = False
        self.auto_value = 0

    def on_scale(self, val):
        v = int(float(val))
        self.progress.set_value(v)
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

    def toggle_auto(self):
        self.auto_running = not self.auto_running
        if self.auto_running:
            self.btn_auto.set_text("■  СТОП")
            self.btn_auto.set_color(ACCENT)
            self.auto_value = 0
            self._auto_step()
        else:
            self.btn_auto.set_text("▶  АВТО")
            self.btn_auto.set_color(GREEN)

    def _auto_step(self):
        if not self.auto_running:
            return
        self.auto_value = (self.auto_value + 3) % 101
        self.scale.set(self.auto_value)
        self.on_scale(self.auto_value)
        self.root.after(50, self._auto_step)

    def reset(self):
        self.auto_running = False
        self.btn_auto.set_text("▶  АВТО")
        self.btn_auto.set_color(GREEN)
        self.scale.set(0)
        self.on_scale(0)


def main():
    root = tk.Tk()
    App(root)
    root.mainloop()


if __name__ == "__main__":
    main()