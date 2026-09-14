"""
ОКФРС. ПЗ №1. Доп. задание 4.
Компонентом TrackBar задавать размер (радиус) круга на форме.
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
    MIN_R = 10
    MAX_R = 220
    CX, CY = 500, 420   # центр круга

    def __init__(self, root):
        self.root = root
        root.title("ОКФРС · ПЗ1 · Доп 4 · Радиус круга через TrackBar")
        root.geometry("1000x780")
        root.resizable(False, False)

        self.canvas = tk.Canvas(root, width=1000, height=780,
                                highlightthickness=0, bg=BG_TOP)
        self.canvas.pack(fill="both", expand=True)

        for i in range(780):
            self.canvas.create_line(0, i, 1000, i,
                                    fill=lerp(BG_TOP, BG_BOTTOM, i/780))

        # заголовок
        self.canvas.create_text(500, 50,
                                text="РАДИУС КРУГА ЧЕРЕЗ TRACKBAR",
                                fill=TEXT_MAIN,
                                font=("Segoe UI", 22, "bold"))
        self.canvas.create_text(500, 84,
                                text="ОКФРС · ПЗ №1 · Доп 4 · ползунок задаёт радиус",
                                fill=TEXT_DIM, font=("Segoe UI", 10))
        self.canvas.create_line(250, 108, 750, 108, fill=NEON, width=2)
        self.canvas.create_line(250, 110, 750, 110,
                                fill=lerp(NEON, BG_TOP, 0.7))

        # ---- Поле для круга ----
        self.canvas.create_rectangle(50, 130, 950, 630,
                                     fill=PANEL_BG, outline=PANEL_BRD)

        # круг с неоновым свечением
        self.glow_ids = []
        for i in range(6, 0, -1):
            item = self.canvas.create_oval(
                self.CX, self.CY, self.CX, self.CY,
                outline=lerp(NEON, PANEL_BG, i*0.15), width=1)
            self.glow_ids.append(item)

        # сам круг
        self.circle_id = self.canvas.create_oval(
            self.CX, self.CY, self.CX, self.CY,
            fill=GREEN, outline=lerp(GREEN, "#ffffff", 0.5), width=2)

        # блик на круге
        self.gloss_id = self.canvas.create_oval(
            self.CX, self.CY, self.CX, self.CY,
            fill=lerp(GREEN, "#ffffff", 0.35), outline="")

        # центр (крестик)
        self.canvas.create_line(self.CX-8, self.CY, self.CX+8, self.CY,
                                fill=TEXT_DIM)
        self.canvas.create_line(self.CX, self.CY-8, self.CX, self.CY+8,
                                fill=TEXT_DIM)

        # ---- Значение радиуса ----
        self.radius_lbl = self.canvas.create_text(
            500, 670,
            text="Радиус: 50",
            fill=GREEN, font=("Consolas", 20, "bold"))

        # ---- TrackBar ----
        self.canvas.create_text(150, 710,
                                text="▸ РАДИУС (10..220)",
                                fill=NEON,
                                font=("Segoe UI", 10, "bold"), anchor="w")
        self.scale = tk.Scale(root, from_=self.MIN_R, to=self.MAX_R,
                              orient="horizontal",
                              bg=PANEL_BG, fg=TEXT_MAIN,
                              troughcolor="#060a16",
                              highlightthickness=0, bd=0,
                              length=700, activebackground=ACCENT,
                              font=("Segoe UI", 10),
                              command=self.on_scale)
        self.scale.set(50)
        self.canvas.create_window(150, 735,
                                  window=self.scale, anchor="nw")

        self.radius = 50
        self.update_circle()

    def update_circle(self):
        r = self.radius
        cx, cy = self.CX, self.CY

        # основной круг
        self.canvas.coords(self.circle_id,
                           cx - r, cy - r, cx + r, cy + r)
        # блик — уменьшенный овал внутри, смещённый вверх
        self.canvas.coords(self.gloss_id,
                           cx - r*0.6, cy - r*0.8,
                           cx + r*0.2, cy - r*0.2)

        # цвет по радиусу
        if r < 60:
            col = GREEN
        elif r < 120:
            col = NEON
        elif r < 170:
            col = AMBER
        else:
            col = ACCENT

        self.canvas.itemconfig(self.circle_id, fill=col,
                               outline=lerp(col, "#ffffff", 0.5))
        self.canvas.itemconfig(self.gloss_id,
                               fill=lerp(col, "#ffffff", 0.35))

        # свечение снаружи
        for i, gid in enumerate(self.glow_ids):
            spread = (6 - i) * 4
            self.canvas.coords(gid,
                               cx - r - spread, cy - r - spread,
                               cx + r + spread, cy + r + spread)
            self.canvas.itemconfig(
                gid, outline=lerp(col, PANEL_BG, i * 0.13))

        # подпись
        self.canvas.itemconfig(self.radius_lbl,
                               text=f"Радиус: {r}",
                               fill=col)

    def on_scale(self, val):
        self.radius = int(float(val))
        self.update_circle()


def main():
    root = tk.Tk()
    App(root)
    root.mainloop()


if __name__ == "__main__":
    main()