"""
ОКФРС. ПЗ №1. Доп. задание 6.
Компонентом TrackBar задавать количество кругов на форме —
модель пикового индикатора уровня, как на магнитофонах.

Логика:
  - всего 20 «лампочек» в ряд;
  - загоревшиеся — от зелёного (начало) до красного (пик);
  - ползунок задаёт, сколько лампочек горит.
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

# LED-цвета (от зелёного к красному)
LED_COLORS = [
    "#0e6e3a",  # тёмный зелёный
    "#22c55e",  # зелёный
    "#84cc16",  # лайм
    "#f4b942",  # жёлтый
    "#f97316",  # оранжевый
    "#ef4444",  # красный
    "#b91c1c",  # тёмный красный
]


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
    TOTAL = 20                # всего лампочек
    LED_R = 22                # радиус лампочки
    LED_GAP = 14              # расстояние между
    START_X = 100             # отступ слева
    Y_CENTER = 400            # координата центра лампочек

    def __init__(self, root):
        self.root = root
        root.title("ОКФРС · ПЗ1 · Доп 6 · LED-индикатор уровня")
        root.geometry("1000x800")
        root.resizable(False, False)

        self.canvas = tk.Canvas(root, width=1000, height=800,
                                highlightthickness=0, bg=BG_TOP)
        self.canvas.pack(fill="both", expand=True)

        for i in range(800):
            self.canvas.create_line(0, i, 1000, i,
                                    fill=lerp(BG_TOP, BG_BOTTOM, i/800))

        # заголовок
        self.canvas.create_text(500, 50,
                                text="LED-ИНДИКАТОР УРОВНЯ",
                                fill=TEXT_MAIN,
                                font=("Segoe UI", 22, "bold"))
        self.canvas.create_text(500, 84,
                                text="ОКФРС · ПЗ №1 · Доп 6 · количество кругов задаётся TrackBar",
                                fill=TEXT_DIM, font=("Segoe UI", 10))
        self.canvas.create_line(200, 108, 800, 108, fill=NEON, width=2)
        self.canvas.create_line(200, 110, 800, 110,
                                fill=lerp(NEON, BG_TOP, 0.7))

        # ---- Панель «магнитофон» ----
        self.canvas.create_rectangle(50, 150, 950, 580,
                                     fill=PANEL_BG, outline=PANEL_BRD)
        # внутренняя рамка «шкалы»
        self.canvas.create_rectangle(70, 170, 930, 560,
                                     fill="#050812",
                                     outline="#2a1a0a", width=2)

        # подписи разделов: GREEN / YELLOW / RED
        self.canvas.create_text(200, 220, text="GREEN",
                                fill=GREEN, font=("Consolas", 12, "bold"))
        self.canvas.create_text(500, 220, text="YELLOW",
                                fill=AMBER, font=("Consolas", 12, "bold"))
        self.canvas.create_text(800, 220, text="RED",
                                fill=ACCENT, font=("Consolas", 12, "bold"))

        # Разделительные линии между зонами (визуально)
        for x in (330, 670):
            self.canvas.create_line(x, 200, x, 540,
                                    fill="#3a4363", dash=(4, 4))

        # Заголовок панели
        self.canvas.create_text(500, 180, text="VU METER  ·  PEAK LEVEL",
                                fill=AMBER, font=("Consolas", 10, "italic"))

        # ---- Лампочки ----
        self.led_ids = []
        total_w = self.TOTAL * (2*self.LED_R) + (self.TOTAL-1) * self.LED_GAP
        start_x = (1000 - total_w) // 2 + self.LED_R

        for i in range(self.TOTAL):
            x = start_x + i * (2*self.LED_R + self.LED_GAP)
            y = self.Y_CENTER

            # тень
            self.canvas.create_oval(
                x - self.LED_R + 2, y - self.LED_R + 2,
                x + self.LED_R + 2, y + self.LED_R + 2,
                fill="#02040a", outline="")

            # корпус лампочки (обводка)
            self.canvas.create_oval(
                x - self.LED_R - 3, y - self.LED_R - 3,
                x + self.LED_R + 3, y + self.LED_R + 3,
                fill="#1a2035", outline="#3a4363", width=2)

            # сама лампочка (заливка меняется)
            led = self.canvas.create_oval(
                x - self.LED_R, y - self.LED_R,
                x + self.LED_R, y + self.LED_R,
                fill="#0a0f1a", outline="")
            self.led_ids.append(led)

            # блик на лампочке (статичный)
            self.canvas.create_oval(
                x - self.LED_R*0.4, y - self.LED_R*0.7,
                x + self.LED_R*0.1, y - self.LED_R*0.2,
                fill="#2a3a55", outline="")

        # ---- Подпись количества ----
        self.count_lbl = self.canvas.create_text(
            500, 620,
            text="Горит: 0 / 20",
            fill=GREEN, font=("Consolas", 20, "bold"))

        # Уровень в «dB» — от -40 до 0
        self.db_lbl = self.canvas.create_text(
            500, 655,
            text="Уровень: -40 dB",
            fill=TEXT_DIM, font=("Consolas", 12))

        # ---- TrackBar ----
        self.canvas.create_text(150, 700,
                                text="▸ КОЛИЧЕСТВО ГОРЯЩИХ ЛАМПОЧЕК (0 .. 20)",
                                fill=NEON,
                                font=("Segoe UI", 10, "bold"), anchor="w")
        self.scale = tk.Scale(root, from_=0, to=self.TOTAL,
                              orient="horizontal",
                              bg=PANEL_BG, fg=TEXT_MAIN,
                              troughcolor="#060a16",
                              highlightthickness=0, bd=0,
                              length=700, activebackground=ACCENT,
                              font=("Segoe UI", 10),
                              command=self.on_scale)
        self.scale.set(0)
        self.canvas.create_window(150, 725,
                                  window=self.scale, anchor="nw")

        # ---- Кнопки ----
        btn_max = NeonButton(root, "MAX PEAK",
                             command=lambda: self.set_count(self.TOTAL),
                             width=180, height=48, color=ACCENT)
        self.canvas.create_window(290, 785, window=btn_max)

        btn_reset = NeonButton(root, "↺ RESET",
                               command=lambda: self.set_count(0),
                               width=180, height=48, color=AMBER)
        self.canvas.create_window(500, 785, window=btn_reset)

        btn_demo = NeonButton(root, "▶ ДЕМО",
                              command=self.demo_cycle,
                              width=180, height=48, color=GREEN)
        self.canvas.create_window(710, 785, window=btn_demo)

        self.count = 0
        self.demo_running = False
        self.update_leds()

    def update_leds(self):
        # Цвет лампочки по её позиции
        for i, led in enumerate(self.led_ids):
            if i < self.count:
                # горит — определяем цвет по позиции
                zone = i / self.TOTAL
                if zone < 0.5:
                    col = LED_COLORS[1]     # зелёный
                elif zone < 0.75:
                    col = LED_COLORS[3]     # жёлтый
                elif zone < 0.9:
                    col = LED_COLORS[4]     # оранжевый
                else:
                    col = LED_COLORS[5]     # красный
                self.canvas.itemconfig(led, fill=col)
            else:
                # потушена — тёмный оттенок нужного цвета
                zone = i / self.TOTAL
                if zone < 0.5:
                    col = "#0e2a1e"   # тёмно-зелёный
                elif zone < 0.75:
                    col = "#2a2210"   # тёмно-жёлтый
                else:
                    col = "#2a1010"   # тёмно-красный
                self.canvas.itemconfig(led, fill=col)

        # подписи
        self.canvas.itemconfig(self.count_lbl,
                               text=f"Горит: {self.count} / {self.TOTAL}")
        # dB = от -40 до 0
        db = -40 + int(self.count / self.TOTAL * 40)
        self.canvas.itemconfig(self.db_lbl, text=f"Уровень: {db} dB")

        # цвет подписи
        if self.count <= 10:
            col = GREEN
        elif self.count <= 15:
            col = AMBER
        else:
            col = ACCENT
        self.canvas.itemconfig(self.count_lbl, fill=col)

    def on_scale(self, val):
        self.count = int(float(val))
        self.update_leds()

    def set_count(self, v):
        v = max(0, min(self.TOTAL, v))
        self.scale.set(v)
        self.count = v
        self.update_leds()

    def demo_cycle(self):
        if self.demo_running:
            return
        self.demo_running = True
        self._demo_step(0)

    def _demo_step(self, i):
        # чередуем набор и сброс
        if i <= self.TOTAL:
            self.set_count(i)
            self.root.after(80, lambda: self._demo_step(i+1))
        elif i <= self.TOTAL * 2:
            self.set_count(2 * self.TOTAL - i)
            self.root.after(60, lambda: self._demo_step(i+1))
        else:
            self.demo_running = False


def main():
    root = tk.Tk()
    App(root)
    root.mainloop()


if __name__ == "__main__":
    main()