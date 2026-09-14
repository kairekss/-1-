"""
ОКФРС. ПЗ №1. Доп. задание 3.
Изменить цвет зелёной полоски ProgressBar.
Реализованы разные темы: зелёная, синяя, фиолетовая, красная, радуга.
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
                 width=180, height=50, color=ACCENT):
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


# ---------- PROGRESSBAR ----------
class ProgressBar(tk.Canvas):
    THEMES = {
        "green":  (GREEN, GREEN),
        "blue":   ("#3b82f6", "#1e40af"),
        "purple": ("#a855f7", "#6d28d9"),
        "red":    ("#ef4444", "#991b1b"),
        "amber":  (AMBER, "#92400e"),
        "rainbow": None,  # особая логика
    }

    def __init__(self, parent, width=680, height=44):
        super().__init__(parent, width=width, height=height,
                         bg=PANEL_BG, highlightthickness=0)
        self.w, self.h = width, height
        self.value = 0
        self.theme = "green"
        self._draw()

    def set_value(self, val):
        self.value = max(0, min(100, val))
        self._draw()

    def set_theme(self, name):
        if name in self.THEMES:
            self.theme = name
            self._draw()

    def _color_at(self, t):
        """Цвет в точке 0..1 в зависимости от темы."""
        if self.theme == "rainbow":
            # HSV-круг через HSL
            import colorsys
            r, g, b = colorsys.hsv_to_rgb(t, 0.9, 0.95)
            return "#{:02x}{:02x}{:02x}".format(
                int(r*255), int(g*255), int(b*255))
        c1, c2 = self.THEMES[self.theme]
        # градиент от c2 (тёмнее) к c1 (ярче)
        return lerp(c1, c2, t)

    def _draw(self):
        self.delete("all")
        # фон
        self.create_rectangle(0, 0, self.w, self.h,
                              fill="#060a16", outline=PANEL_BRD)

        fill_w = int(self.w * self.value / 100)
        if fill_w > 0:
            steps = max(fill_w // 3, 1)
            for i in range(steps):
                t = i / steps
                x1 = int(i * fill_w / steps)
                x2 = int((i + 1) * fill_w / steps)
                c = self._color_at(t)
                self.create_rectangle(x1, 2, x2, self.h - 2,
                                      fill=c, outline="")

            # блик сверху
            top_color = self._color_at(0)
            self.create_rectangle(0, 2, fill_w, self.h // 2,
                                  fill=lerp(top_color, "#ffffff", 0.3),
                                  outline="")

        # рамка
        self.create_rectangle(0, 0, self.w - 1, self.h - 1,
                              outline=PANEL_BRD, width=1)

        # текст-процент
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
        root.title("ОКФРС · ПЗ1 · Доп 3 · Изменение цвета ProgressBar")
        root.geometry("1000x720")
        root.resizable(False, False)

        self.canvas = tk.Canvas(root, width=1000, height=720,
                                highlightthickness=0, bg=BG_TOP)
        self.canvas.pack(fill="both", expand=True)

        for i in range(720):
            self.canvas.create_line(0, i, 1000, i,
                                    fill=lerp(BG_TOP, BG_BOTTOM, i/720))

        # заголовок
        self.canvas.create_text(500, 50,
                                text="ЦВЕТ PROGRESSBAR",
                                fill=TEXT_MAIN,
                                font=("Segoe UI", 22, "bold"))
        self.canvas.create_text(500, 84,
                                text="ОКФРС · ПЗ №1 · Доп 3 · изменение цвета заливки",
                                fill=TEXT_DIM, font=("Segoe UI", 10))
        self.canvas.create_line(250, 108, 750, 108, fill=NEON, width=2)
        self.canvas.create_line(250, 110, 750, 110,
                                fill=lerp(NEON, BG_TOP, 0.7))

        # текущая тема
        self.canvas.create_text(500, 140,
                                text="▸ ЦВЕТ: ЗЕЛЁНЫЙ",
                                fill=GREEN,
                                font=("Segoe UI", 11, "bold"))
        self.theme_lbl = self.canvas.create_text(
            500, 165,
            text="ЗЕЛЁНЫЙ (классический)",
            fill=GREEN,
            font=("Consolas", 14, "bold"))

        # ProgressBar
        self.canvas.create_rectangle(155, 220, 845, 285,
                                     fill=PANEL_BG, outline=PANEL_BRD)
        self.progress = ProgressBar(root, width=670, height=44)
        self.canvas.create_window(170, 230,
                                  window=self.progress, anchor="nw")

        # TrackBar
        self.canvas.create_text(150, 320,
                                text="▸ ЗНАЧЕНИЕ ПРОГРЕССА",
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
        self.canvas.create_window(150, 345,
                                  window=self.scale, anchor="nw")

        # Большая цифра
        self.value_lbl = self.canvas.create_text(
            500, 445, text="0 %",
            fill=GREEN, font=("Consolas", 48, "bold"))

        # Кнопки смены темы
        self.canvas.create_text(500, 500,
                                text="▸ ЦВЕТОВЫЕ ТЕМЫ",
                                fill=NEON,
                                font=("Segoe UI", 10, "bold"))

        themes = [
            ("ЗЕЛЁНЫЙ", "green", GREEN),
            ("СИНИЙ",   "blue",  "#3b82f6"),
            ("ФИОЛЕТ",  "purple","#a855f7"),
            ("КРАСНЫЙ", "red",   "#ef4444"),
            ("ЖЁЛТЫЙ",  "amber", AMBER),
            ("РАДУГА",  "rainbow", "#ffffff"),
        ]
        # 3 сверху, 3 снизу
        for i, (label, key, col) in enumerate(themes):
            x = 250 + (i % 3) * 250
            y = 540 + (i // 3) * 65
            btn = NeonButton(root, label,
                             command=lambda k=key, c=col, l=label:
                                 self.set_theme(k, c, l),
                             width=180, height=48, color=col)
            self.canvas.create_window(x, y, window=btn)

        self.canvas.create_text(500, 700,
                                text="© ОКФРС · ПЗ №1 · Доп 3",
                                fill="#2f3a5a", font=("Segoe UI", 9))

    def on_scale(self, val):
        v = int(float(val))
        self.progress.set_value(v)
        self.canvas.itemconfig(self.value_lbl, text=f"{v} %")

    def set_theme(self, key, color, label):
        self.progress.set_theme(key)
        self.progress.set_value(int(float(self.scale.get())))
        self.canvas.itemconfig(self.theme_lbl, text=label, fill=color)
        self.canvas.itemconfig(self.value_lbl, fill=color)


def main():
    root = tk.Tk()
    App(root)
    root.mainloop()


if __name__ == "__main__":
    main()