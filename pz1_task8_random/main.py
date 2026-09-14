"""
ОКФРС. ПЗ №1. Задание 8.
TrackBar задаёт область случайных чисел, ProgressBar показывает
смену состояний, кнопка «Сброс» очищает результат.
"""
import tkinter as tk
import random


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
        self.create_rectangle(0, 0, self.w, self.h,
                              fill="#060a16", outline=PANEL_BRD)

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
            self.create_rectangle(0, 2, fill_w, self.h // 2,
                                  fill=lerp(col, "#ffffff", 0.25), outline="")

        self.create_rectangle(0, 0, self.w - 1, self.h - 1,
                              outline=PANEL_BRD, width=1)

        if self.value > 12:
            self.create_text(
                8, self.h // 2,
                text=f"{self.value}%",
                fill="#ffffff", anchor="w",
                font=("Consolas", 12, "bold"))


# ---------- ГЛАВНОЕ ОКНО ----------
class App:
    MAX_VALUES = 20

    def __init__(self, root):
        self.root = root
        root.title("ОКФРС · ПЗ1 · Задание 8 · Случайные числа + ProgressBar")
        root.geometry("1050x720")
        root.resizable(False, False)

        self.canvas = tk.Canvas(root, width=1050, height=720,
                                highlightthickness=0, bg=BG_TOP)
        self.canvas.pack(fill="both", expand=True)

        for i in range(720):
            self.canvas.create_line(0, i, 1050, i,
                                    fill=lerp(BG_TOP, BG_BOTTOM, i/720))

        # заголовок
        self.canvas.create_text(525, 50,
                                text="СЛУЧАЙНЫЕ ЧИСЛА + PROGRESSBAR",
                                fill=TEXT_MAIN,
                                font=("Segoe UI", 22, "bold"))
        self.canvas.create_text(525, 84,
                                text="ОКФРС · ПЗ №1 · Задание 8 · диапазон, прогресс, сброс",
                                fill=TEXT_DIM, font=("Segoe UI", 10))
        self.canvas.create_line(250, 108, 800, 108, fill=NEON, width=2)
        self.canvas.create_line(250, 110, 800, 110,
                                fill=lerp(NEON, BG_TOP, 0.7))

        # ---- TrackBar диапазона ----
        self.canvas.create_text(160, 140,
                                text="▸ МАКСИМАЛЬНОЕ ЗНАЧЕНИЕ (диапазон 0..N)",
                                fill=NEON,
                                font=("Segoe UI", 10, "bold"), anchor="w")

        self.scale = tk.Scale(root, from_=10, to=100, orient="horizontal",
                              bg=PANEL_BG, fg=TEXT_MAIN,
                              troughcolor="#060a16",
                              highlightthickness=0, bd=0,
                              length=720, activebackground=ACCENT,
                              font=("Segoe UI", 10),
                              command=self.on_scale)
        self.scale.set(100)
        self.canvas.create_window(160, 160,
                                  window=self.scale, anchor="nw")

        # ---- ProgressBar ----
        self.canvas.create_text(160, 240,
                                text="▸ PROGRESSBAR (заполняется по мере генерации)",
                                fill=NEON,
                                font=("Segoe UI", 10, "bold"), anchor="w")

        self.canvas.create_rectangle(155, 265, 905, 320,
                                     fill=PANEL_BG, outline=PANEL_BRD)
        self.progress = ProgressBar(root, width=740, height=44)
        self.canvas.create_window(160, 272,
                                  window=self.progress, anchor="nw")

        # ---- Список сгенерированных чисел ----
        self.canvas.create_text(160, 350,
                                text="▸ СГЕНЕРИРОВАННЫЕ ЧИСЛА",
                                fill=NEON,
                                font=("Segoe UI", 10, "bold"), anchor="w")

        self.canvas.create_rectangle(155, 375, 905, 590,
                                     fill=PANEL_BG, outline=PANEL_BRD)

        self.memo = tk.Text(root,
                            bg=PANEL_BG, fg=NEON,
                            insertbackground=TEXT_MAIN,
                            font=("Consolas", 13),
                            bd=0, highlightthickness=0,
                            wrap="word")
        self.canvas.create_window(170, 388, window=self.memo,
                                  anchor="nw", width=720, height=190)

        # ---- Кнопки ----
        btn_gen = NeonButton(root, "+  СГЕНЕРИРОВАТЬ",
                             command=self.generate,
                             width=280, height=54, color=ACCENT)
        self.canvas.create_window(340, 640, window=btn_gen)

        btn_reset = NeonButton(root, "↺  СБРОС",
                               command=self.reset,
                               width=200, height=54, color=AMBER)
        self.canvas.create_window(650, 640, window=btn_reset)

        self.canvas.create_text(525, 700,
                                text="© ОКФРС · ПЗ №1 · Задание 8",
                                fill="#2f3a5a", font=("Segoe UI", 9))

        self.count = 0
        self.max_count = 20  # макс. чисел до полного прогресса

    def on_scale(self, val):
        # просто обновляем подпись диапазона, ничего не сбрасываем
        pass

    def generate(self):
        if self.count >= self.max_count:
            return

        high = int(self.scale.get())
        n = random.randint(0, high)
        self.memo.insert(tk.END, f"{n:>4}   ")
        self.count += 1

        # обновляем прогресс
        percent = int(self.count / self.max_count * 100)
        self.progress.set_value(percent)

    def reset(self):
        self.count = 0
        self.memo.delete(1.0, tk.END)
        self.progress.set_value(0)


def main():
    root = tk.Tk()
    App(root)
    root.mainloop()


if __name__ == "__main__":
    main()