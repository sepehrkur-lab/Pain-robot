# face_rinnegan.py
# Kivy widget that draws two centered Rinnegan-style eyes.
from kivy.uix.widget import Widget
from kivy.graphics import Color, Ellipse, Rectangle, Line
from kivy.clock import Clock
import random, math, time

class RinneganWidget(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.size_hint = (1, 1)
        self.emotion = "neutral"
        # timing
        self.px = 0.0
        self.py = 0.0
        self.px_target = 0.0
        self.py_target = 0.0
        self.look_timer = 0.0
        self.look_interval = 1.4
        self.blink = 0.0
        self.blinking = False
        self.next_blink = 2.0 + random.random()*3.0
        self.last = time.time()
        # schedule redraw
        Clock.schedule_interval(self.draw, 1/60.)

    def set_emotion(self, e):
        self.emotion = e

    def update(self, dt):
        # update wander/look
        self.look_timer += dt
        if self.look_timer >= self.look_interval:
            self.look_timer = 0.0
            self.look_interval = 1.0 + random.random()*2.0
            self.px_target = random.uniform(-0.8, 0.8)
            self.py_target = random.uniform(-0.4, 0.4)
        # smooth approach
        speed = 4.0 * dt * 60.0 / 60.0
        self.px += (self.px_target - self.px) * min(1.0, speed*0.12)
        self.py += (self.py_target - self.py) * min(1.0, speed*0.12)
        # blink
        self.next_blink -= dt
        if self.next_blink <= 0 and not self.blinking:
            self.blinking = True
            self.blink = 0.0
            self.next_blink = 2.0 + random.random()*3.0
        if self.blinking:
            self.blink += 8.0 * dt
            if self.blink >= 1.0:
                self.blink = 0.0
                self.blinking = False

    def draw(self, dt):
        self.canvas.clear()
        w, h = self.width, self.height
        cx = w/2
        cy = h/2
        # eye sizes
        eye_w = min(w*0.38, 260)
        eye_h = min(h*0.38, 160)
        gap = 40
        left_x = cx - (eye_w + gap/2)
        right_x = cx + (gap/2)
        top_y = cy - eye_h/2
        # draw background
        with self.canvas:
            Color(18/255,18/255,18/255)
            Rectangle(pos=self.pos, size=self.size)
            # left eye base
            Color(200/255,170/255,255/255)
            Ellipse(pos=(left_x, top_y), size=(eye_w, eye_h))
            # right eye base
            Ellipse(pos=(right_x, top_y), size=(eye_w, eye_h))
            # rings (both)
            for i in range(5):
                factor = 1.0 - 0.12*i
                rw = eye_w*0.88*factor
                rh = eye_h*0.88*factor
                rx_left = left_x + (eye_w-rw)/2
                ry = top_y + (eye_h-rh)/2
                Color((95/255,60/255,180/255) if i%2==0 else (140/255,100/255,220/255))
                Line(ellipse=(rx_left, ry, rw, rh), width=2)
                rx_right = right_x + (eye_w-rw)/2
                Line(ellipse=(rx_right, ry, rw, rh), width=2)
            # pupil positions (shared movement)
            max_off_x = eye_w * 0.18
            max_off_y = eye_h * 0.15
            ox = int(self.px * max_off_x)
            oy = int(self.py * max_off_y)
            # left pupil
            px = int(left_x + eye_w/2 + ox)
            py = int(top_y + eye_h/2 + oy)
            Color(16/255,10/255,18/255)
            Ellipse(pos=(px-8, py-8), size=(16,16))
            # right pupil
            px2 = int(right_x + eye_w/2 + ox)
            py2 = int(top_y + eye_h/2 + oy)
            Ellipse(pos=(px2-8, py2-8), size=(16,16))
            # highlights
            Color(1,1,1,0.12)
            Ellipse(pos=(left_x + eye_w*0.12, top_y + eye_h*0.08), size=(eye_w*0.18, eye_h*0.12))
            Ellipse(pos=(right_x + eye_w*0.12, top_y + eye_h*0.08), size=(eye_w*0.18, eye_h*0.12))
            # blink cover
            if self.blink > 0:
                b = min(1.0, self.blink)
                top_h = int(b * (eye_h * 0.6))
                Color(18/255,18/255,18/255)
                Rectangle(pos=(left_x, top_y), size=(eye_w, top_h))
                Rectangle(pos=(right_x, top_y), size=(eye_w, top_h))
