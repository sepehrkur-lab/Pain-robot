# main.py
from kivy.app import App
from kivy.clock import Clock
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.core.window import Window

from face_rinnegan import RinneganWidget
from stt_tts import TTS_STT
from ai_client import AIClient
from memory import Memory

Window.clearcolor = (18/255, 18/255, 18/255, 1)
Window.size = (400, 800)

# Singletons
tts = TTS_STT()
ai = AIClient()
memory = Memory("pain_memory.db")

EMOTIONS = ["neutral", "happy", "sad", "surprised", "angry", "thinking"]

class StartScreen(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)
        layout = BoxLayout(orientation='vertical', padding=20, spacing=12)
        layout.add_widget(Label(text="Pain Robot", font_size=34))
        b_start = Button(text="Start", size_hint=(1, 0.18))
        b_sit = Button(text="Sitting", size_hint=(1, 0.18))
        b_exit = Button(text="Exit", size_hint=(1, 0.18))
        layout.add_widget(b_start)
        layout.add_widget(b_sit)
        layout.add_widget(b_exit)
        self.add_widget(layout)
        b_start.bind(on_release=self.start_robot)
        b_exit.bind(on_release=lambda *_: App.get_running_app().stop())
        b_sit.bind(on_release=self.sit_action)

    def sit_action(self, *_):
        tts.say("Entering sitting mode.")
    def start_robot(self, *_):
        # request permissions will be handled on Android runtime (via pyjnius in stt_tts)
        self.manager.current = 'face'

class FaceScreen(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)
        self.widget = RinneganWidget()
        self.add_widget(self.widget)
        Clock.schedule_interval(self.update, 1/60.)
        Clock.schedule_once(lambda dt: self.on_startup(), 0.8)
        # start STT listener in background
        tts.start_listening(self.on_speech)

    def on_startup(self):
        tts.say("Pain robot activated.")
        # the special message about Sepehr
        tts.say("Sepehr is my creator. He built me at age fourteen. He is from Ravansar in Kermanshah province. He is a Kurdish boy.")

    def on_speech(self, text):
        # called when STT has recognized text (english)
        if not text:
            return
        txt = text.lower()
        # wake word
        if "pain" in txt:
            tts.say("Yes. I am listening.")
            return
        # check memory
        ans = memory.get(txt)
        if ans:
            tts.say(ans)
            return
        # ask AI online
        resp = ai.ask(txt)
        if resp:
            memory.save(txt, resp)
            tts.say(resp)
        else:
            tts.say("I couldn't fetch an answer right now.")

    def update(self, dt):
        self.widget.update(dt)

class PainApp(App):
    def build(self):
        sm = ScreenManager(transition=FadeTransition())
        sm.add_widget(StartScreen(name='start'))
        sm.add_widget(FaceScreen(name='face'))
        return sm

if __name__ == '__main__':
    PainApp().run()
