"""
ОКФРС. ПЗ №1. Задание 9.
TrackBar задаёт значения цветовой палитры RGB (+коды цвета, значения RGB).
"""
import tkinter as tk


# ---------- ПАЛИТРА ----------
BG_TOP     = "#0a0e1c"
BG_BOTTOM  = "#141a30"
PANEL_BG   = "#0f1425"
PANEL_BRD  = "#2a3150"
NEON       = "#22d3ee"
TEXT_MAIN  = "#eef2ff"
TEXT_DIM   = "#5c6a90"
RED_C      = "#ff3860"
GREEN_C    = "#22c55e"
BLUE_C     = "#3b82f6"


def lerp(c1, c2, t):
    r1, g1, b1 = int(c1[1:3],16), int(c1[3:5],16), int(c1[5:7],16)
    r2, g2, b2 = int(c2[1:3],16), int(c2[3:5],16), int(c2[5:7],16)
    return "#{:02x}{:02x}{:02x}".format(
        int(r1+(r2-r1)*t), int(g1+(g2-g1)*t), int(b1+(b2-b1)*t))


# ---------- КНОПКА ----------
class NeonButton(tk.Canvas):
    def __init__(self, parent, text, command,
                 width=200, height=50, color=NEON):
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


# ---------- КАНАЛ RGB (ползунок + значение) ----------
class RGBChannel(tk.Canvas):
    def __init__(self, parent, label, color, on_change):
        super().__init__(parent, width=560, height=90,
                         bg=PANEL_BG, highlightthickness=0)
        self.label = label
        self.color = color
        self.on_change = on_change
        self.value = 0
        self._draw()

    def _draw(self):
        self.delete("all")
        w = 560

        # подпись
        self.create_text(10, 18, text=self.label, anchor="w",
                         fill=self.color,
                         font=("Segoe UI", 13, "bold"))

        # текущее значение
        self.create_text(w - 10, 18, text=f"{self.value:>3}",
                         anchor="e", fill="#ffffff",
                         font=("Consolas", 16, "bold"))

        # шкала (трек)
        bar_x0, bar_y0 = 10, 50
        bar_x1, bar_y1 = w - 10, 70
        self.create_rectangle(bar_x0, bar_y0, bar_x1, bar_y1,
                              fill="#060a16", outline=PANEL_BRD)

        # заполнение
        fill_w = int((bar_x1 - bar_x0) * self.value / 255)
        # градиент в цвет канала
        steps = max(fill_w // 4, 1)
        for i in range(steps):
            t = i / steps
            x1 = bar_x0 + int(i * fill_w / steps)
            x2 = bar_x0 + int((i + 1) * fill_w / steps)
            c = lerp("#060a16", self.color, t)
            self.create_rectangle(x1, bar_y0+2, x2, bar_y1-2,
                                  fill=c, outline="")

        # риски 0, 64, 128, 192, 255
        for v in (0, 64, 128, 192, 255):
            x = bar_x0 + int((bar_x1 - bar_x0) * v / 255)
            self.create_line(x, bar_y1, x, bar_y1+6, fill="#3a4363")
            self.create_text(x, 82, text=str(v), fill=TEXT_DIM,
                             font=("Consolas", 8))

    def set_value(self, v):
        self.value = max(0, min(255, v))
        self._draw()


# ---------- ГЛАВНОЕ ОКНО ----------
class App:
    def __init__(self, root):
        self.root = root
        root.title("ОКФРС · ПЗ1 · Задание 9 · RGB-палитра")
        root.geometry("1150x700")
        root.resizable(False, False)

        self.canvas = tk.Canvas(root, width=1150, height=700,
                                highlightthickness=0, bg=BG_TOP)
        self.canvas.pack(fill="both", expand=True)

        for i in range(700):
            self.canvas.create_line(0, i, 1150, i,
                                    fill=lerp(BG_TOP, BG_BOTTOM, i/700))

        # заголовок
        self.canvas.create_text(575, 50,
                                text="RGB-ПАЛИТРА",
                                fill=TEXT_MAIN,
                                font=("Segoe UI", 22, "bold"))
        self.canvas.create_text(575, 84,
                                text="ОКФРС · ПЗ №1 · Задание 9 · TrackBar -> RGB-цвет",
                                fill=TEXT_DIM, font=("Segoe UI", 10))
        self.canvas.create_line(300, 108, 850, 108, fill=NEON, width=2)
        self.canvas.create_line(300, 110, 850, 110,
                                fill=lerp(NEON, BG_TOP, 0.7))

        # ---- ЛЕВАЯ ПАНЕЛЬ: ползунки каналов ----
        self.canvas.create_text(60, 140,
                                text="▸ КАНАЛЫ RGB",
                                fill=NEON,
                                font=("Segoe UI", 10, "bold"), anchor="w")

        self.canvas.create_rectangle(50, 165, 630, 480,
                                     fill=PANEL_BG, outline=PANEL_BRD)

        # R
        self.ch_r_scale = tk.Scale(root, from_=0, to=255, orient="horizontal",
                                   showvalue=0,
                                   bg=PANEL_BG, fg=TEXT_MAIN,
                                   troughcolor="#060a16",
                                   highlightthickness=0, bd=0,
                                   length=560, activebackground=RED_C,
                                   command=self.on_r)
        self.ch_r_scale.set(255)
        self.canvas.create_window(60, 175,
                                  window=self.ch_r_scale, anchor="nw")

        # G
        self.ch_g_scale = tk.Scale(root, from_=0, to=255, orient="horizontal",
                                   showvalue=0,
                                   bg=PANEL_BG, fg=TEXT_MAIN,
                                   troughcolor="#060a16",
                                   highlightthickness=0, bd=0,
                                   length=560, activebackground=GREEN_C,
                                   command=self.on_g)
        self.ch_g_scale.set(0)
        self.canvas.create_window(60, 280,
                                  window=self.ch_g_scale, anchor="nw")

        # B
        self.ch_b_scale = tk.Scale(root, from_=0, to=255, orient="horizontal",
                                   showvalue=0,
                                   bg=PANEL_BG, fg=TEXT_MAIN,
                                   troughcolor="#060a16",
                                   highlightthickness=0, bd=0,
                                   length=560, activebackground=BLUE_C,
                                   command=self.on_b)
        self.ch_b_scale.set(0)
        self.canvas.create_window(60, 385,
                                  window=self.ch_b_scale, anchor="nw")

        # подписи каналов поверх шкал
        self.canvas.create_text(70, 200, text="R", anchor="w",
                                fill=RED_C, font=("Segoe UI", 18, "bold"))
        self.canvas.create_text(70, 305, text="G", anchor="w",
                                fill=GREEN_C, font=("Segoe UI", 18, "bold"))
        self.canvas.create_text(70, 410, text="B", anchor="w",
                                fill=BLUE_C, font=("Segoe UI", 18, "bold"))

        # цифры справа от ползунков
        self.r_lbl = self.canvas.create_text(610, 200, text="255",
                                             anchor="e", fill="#fff",
                                             font=("Consolas", 18, "bold"))
        self.g_lbl = self.canvas.create_text(610, 305, text="0",
                                             anchor="e", fill="#fff",
                                             font=("Consolas", 18, "bold"))
        self.b_lbl = self.canvas.create_text(610, 410, text="0",
                                             anchor="e", fill="#fff",
                                             font=("Consolas", 18, "bold"))

        # ---- ПРАВАЯ ПАНЕЛЬ: превью цвета ----
        self.canvas.create_text(870, 140,
                                text="▸ ЦВЕТ",
                                fill=NEON,
                                font=("Segoe UI", 10, "bold"), anchor="w")

        self.canvas.create_rectangle(640, 165, 1100, 480,
                                     fill=PANEL_BG, outline=PANEL_BRD)

        # квадрат цвета
        self.color_box = self.canvas.create_rectangle(
            680, 200, 1060, 360,
            fill="#ff0000", outline=PANEL_BRD, width=2)

        # HEX-код
        self.hex_lbl = self.canvas.create_text(
            870, 400, text="#FF0000",
            fill="#ffffff", font=("Consolas", 24, "bold"))

        # RGB-код
        self.rgb_lbl = self.canvas.create_text(
            870, 445, text="rgb(255, 0, 0)",
            fill=TEXT_DIM, font=("Consolas", 14))

        # ---- Кнопки предустановок ----
        self.canvas.create_text(60, 510,
                                text="▸ БЫСТРЫЕ ЦВЕТА",
                                fill=NEON,
                                font=("Segoe UI", 10, "bold"), anchor="w")

        presets = [
            ("КРАСНЫЙ",   (255, 0, 0),    RED_C),
            ("ЗЕЛЁНЫЙ",   (0, 255, 0),    GREEN_C),
            ("СИНИЙ",     (0, 0, 255),    BLUE_C),
            ("ЖЁЛТЫЙ",    (255, 255, 0),  "#f4b942"),
            ("БЕЛЫЙ",     (255, 255, 255),"#ffffff"),
            ("ЧЁРНЫЙ",    (0, 0, 0),      "#333333"),
        ]
        x0 = 60
        for i, (label, rgb, col) in enumerate(presets):
            btn = NeonButton(root, label,
                             command=lambda v=rgb: self.set_color(v),
                             width=155, height=48, color=col)
            self.canvas.create_window(x0 + (i % 3) * 175,
                                      555 + (i // 3) * 60,
                                      window=btn)

        self.canvas.create_text(575, 685,
                                text="© ОКФРС · ПЗ №1 · Задание 9",
                                fill="#2f3a5a", font=("Segoe UI", 9))

        # инициализация
        self.update_color()

    def on_r(self, val):
        self.canvas.itemconfig(self.r_lbl, text=str(int(float(val))))
        self.update_color()

    def on_g(self, val):
        self.canvas.itemconfig(self.g_lbl, text=str(int(float(val))))
        self.update_color()

    def on_b(self, val):
        self.canvas.itemconfig(self.b_lbl, text=str(int(float(val))))
        self.update_color()

    def update_color(self):
        r = int(float(self.ch_r_scale.get()))
        g = int(float(self.ch_g_scale.get()))
        b = int(float(self.ch_b_scale.get()))

        hex_color = f"#{r:02X}{g:02X}{b:02X}"

        self.canvas.itemconfig(self.color_box, fill=hex_color)
        self.canvas.itemconfig(self.hex_lbl, text=hex_color)
        self.canvas.itemconfig(self.rgb_lbl,
                               text=f"rgb({r}, {g}, {b})")

        # подсветка HEX-кода тёмным/светлым в зависимости от яркости
        bright = (r*299 + g*587 + b*114) / 1000
        text_col = "#000000" if bright > 150 else "#ffffff"
        self.canvas.itemconfig(self.hex_lbl, fill=text_col)

    def set_color(self, rgb):
        r, g, b = rgb
        self.ch_r_scale.set(r)
        self.ch_g_scale.set(g)
        self.ch_b_scale.set(b)
        self.canvas.itemconfig(self.r_lbl, text=str(r))
        self.canvas.itemconfig(self.g_lbl, text=str(g))
        self.canvas.itemconfig(self.b_lbl, text=str(b))
        self.update_color()


def main():
    root = tk.Tk()
    App(root)
    root.mainloop()


if __name__ == "__main__":
    main()