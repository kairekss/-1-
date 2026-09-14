"""
ОКФРС. ПЗ №1. Доп. задание 7.
Компонентами TrackBar задавать размеры (длина, ширина)
прямоугольника на форме.
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


# ---------- ГЛАВНОЕ ОКНО ----------
class App:
    CX, CY = 500, 340    # центр прямоугольника
    MIN_W, MAX_W = 40, 700
    MIN_H, MAX_H = 30, 380

    def __init__(self, root):
        self.root = root
        root.title("ОКФРС · ПЗ1 · Доп 7 · Размеры прямоугольника")
        root.geometry("1100x820")
        root.resizable(False, False)

        self.canvas = tk.Canvas(root, width=1100, height=820,
                                highlightthickness=0, bg=BG_TOP)
        self.canvas.pack(fill="both", expand=True)

        for i in range(820):
            self.canvas.create_line(0, i, 1100, i,
                                    fill=lerp(BG_TOP, BG_BOTTOM, i/820))

        # заголовок
        self.canvas.create_text(550, 50,
                                text="РАЗМЕРЫ ПРЯМОУГОЛЬНИКА",
                                fill=TEXT_MAIN,
                                font=("Segoe UI", 22, "bold"))
        self.canvas.create_text(550, 84,
                                text="ОКФРС · ПЗ №1 · Доп 7 · два TrackBar → ширина и высота",
                                fill=TEXT_DIM, font=("Segoe UI", 10))
        self.canvas.create_line(300, 108, 800, 108, fill=NEON, width=2)
        self.canvas.create_line(300, 110, 800, 110,
                                fill=lerp(NEON, BG_TOP, 0.7))

        # ---- Поле ----
        self.canvas.create_rectangle(50, 130, 1050, 580,
                                     fill=PANEL_BG, outline=PANEL_BRD)

        # крестик центра
        self.canvas.create_line(self.CX-10, self.CY,
                                self.CX+10, self.CY, fill=TEXT_DIM)
        self.canvas.create_line(self.CX, self.CY-10,
                                self.CX, self.CY+10, fill=TEXT_DIM)

        # свечение (6 слоёв)
        self.glow_ids = []
        for i in range(6, 0, -1):
            item = self.canvas.create_rectangle(
                self.CX, self.CY, self.CX, self.CY,
                outline=lerp(NEON, PANEL_BG, i*0.15), width=1)
            self.glow_ids.append(item)

        # прямоугольник
        self.rect_id = self.canvas.create_rectangle(
            self.CX, self.CY, self.CX, self.CY,
            fill=GREEN, outline=lerp(GREEN, "#ffffff", 0.5), width=2)

        # блик сверху
        self.gloss_id = self.canvas.create_rectangle(
            self.CX, self.CY, self.CX, self.CY,
            fill=lerp(GREEN, "#ffffff", 0.35), outline="")

        # ---- Подписи размеров ----
        self.size_lbl = self.canvas.create_text(
            550, 610,
            text="Ширина: 200  ·  Высота: 120",
            fill=GREEN, font=("Consolas", 20, "bold"))

        # ---- TrackBar ШИРИНА ----
        self.canvas.create_text(150, 660,
                                text="▸ ШИРИНА (40 .. 700)",
                                fill=NEON,
                                font=("Segoe UI", 10, "bold"), anchor="w")
        self.w_scale = tk.Scale(root, from_=self.MIN_W, to=self.MAX_W,
                                orient="horizontal",
                                bg=PANEL_BG, fg=TEXT_MAIN,
                                troughcolor="#060a16",
                                highlightthickness=0, bd=0,
                                length=800, activebackground=ACCENT,
                                font=("Segoe UI", 10),
                                command=self.on_w)
        self.w_scale.set(200)
        self.canvas.create_window(150, 685,
                                  window=self.w_scale, anchor="nw")

        # ---- TrackBar ВЫСОТА ----
        self.canvas.create_text(150, 730,
                                text="▸ ВЫСОТА (30 .. 380)",
                                fill=NEON,
                                font=("Segoe UI", 10, "bold"), anchor="w")
        self.h_scale = tk.Scale(root, from_=self.MIN_H, to=self.MAX_H,
                                orient="horizontal",
                                bg=PANEL_BG, fg=TEXT_MAIN,
                                troughcolor="#060a16",
                                highlightthickness=0, bd=0,
                                length=800, activebackground=ACCENT,
                                font=("Segoe UI", 10),
                                command=self.on_h)
        self.h_scale.set(120)
        self.canvas.create_window(150, 755,
                                  window=self.h_scale, anchor="nw")

        # ---- Кнопки пресетов ----
        self._preset_button("КВАДРАТ 200x200", 200, 200, NEON, 300)
        self._preset_button("ШИРОКИЙ 600x100", 600, 100, GREEN, 500)
        self._preset_button("ВЫСОКИЙ 120x350", 120, 350, AMBER, 700)
        self._preset_button("МИНИ 40x30", 40, 30, ACCENT, 900)

        self.w = 200
        self.h = 120
        self.update_rect()

    def _preset_button(self, label, w, h, color, x):
        btn = NeonButton(self.root, label,
                         command=lambda: self.set_size(w, h),
                         width=180, height=46, color=color)
        self.canvas.create_window(x, 800, window=btn)

    def update_rect(self):
        w, h = self.w, self.h
        cx, cy = self.CX, self.CY
        x1, y1 = cx - w//2, cy - h//2
        x2, y2 = cx + w//2, cy + h//2

        # прямоугольник
        self.canvas.coords(self.rect_id, x1, y1, x2, y2)
        # блик — верхняя полоса внутри
        self.canvas.coords(self.gloss_id,
                           x1 + 4, y1 + 4,
                           x2 - 4, y1 + max(6, h//3))

        # цвет по площади
        area = w * h
        if area < 20000:
            col = GREEN
        elif area < 80000:
            col = NEON
        elif area < 150000:
            col = AMBER
        else:
            col = ACCENT

        self.canvas.itemconfig(self.rect_id, fill=col,
                               outline=lerp(col, "#ffffff", 0.5))
        self.canvas.itemconfig(self.gloss_id,
                               fill=lerp(col, "#ffffff", 0.35))

        # свечение
        for i, gid in enumerate(self.glow_ids):
            spread = (6 - i) * 4
            self.canvas.coords(gid,
                               x1 - spread, y1 - spread,
                               x2 + spread, y2 + spread)
            self.canvas.itemconfig(
                gid, outline=lerp(col, PANEL_BG, i * 0.13))

        # подпись
        self.canvas.itemconfig(
            self.size_lbl,
            text=f"Ширина: {w}  ·  Высота: {h}  ·  Площадь: {area}",
            fill=col)

    def on_w(self, val):
        self.w = int(float(val))
        self.update_rect()

    def on_h(self, val):
        self.h = int(float(val))
        self.update_rect()

    def set_size(self, w, h):
        self.w_scale.set(w)
        self.h_scale.set(h)
        self.w = w
        self.h = h
        self.update_rect()


def main():
    root = tk.Tk()
    App(root)
    root.mainloop()


if __name__ == "__main__":
    main()