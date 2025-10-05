# stt_tts.py
# A small wrapper: on Android uses pyjnius to access TextToSpeech and SpeechRecognizer.
# On desktop it prints actions (fallback).
import threading, time, sys

try:
    from jnius import autoclass, cast
    ANDROID = True
except Exception:
    ANDROID = False

class TTS_STT:
    def __init__(self):
        self.listening = False
        self._callback = None
        if ANDROID:
            # Android TextToSpeech
            PythonActivity = autoclass('org.kivy.android.PythonActivity')
            self.activity = PythonActivity.mActivity
            TextToSpeech = autoclass('android.speech.tts.TextToSpeech')
            Locale = autoclass('java.util.Locale')
            self.tts = TextToSpeech(self.activity, None)
            self.tts.setLanguage(Locale.ENGLISH)
        else:
            self.tts = None

    def say(self, text):
        if ANDROID and self.tts:
            try:
                self.tts.speak(text, 0, None, "utteranceId")
            except Exception:
                print("[TTS ERROR]", text)
        else:
            print("[TTS]", text)

    def _stt_thread(self):
        # Placeholder: real Android continuous STT via pyjnius is complex.
        # For robust STT, implement RecognitionListener in Java/Kotlin (MainActivity) and pass results to Python.
        return

    def start_listening(self, callback):
        # callback(text) will be called on recognized text.
        self._callback = callback
        if ANDROID:
            t = threading.Thread(target=self._android_listen_loop, daemon=True)
            t.start()
        else:
            t = threading.Thread(target=self._desktop_sim, daemon=True)
            t.start()

    def _desktop_sim(self):
        # Desktop fallback: no continuous STT
        while True:
            time.sleep(0.1)

    def _android_listen_loop(self):
        # Placeholder for Android STT loop.
        # Production: implement RecognitionListener in MainActivity and forward results via file/socket/Intent.
        return
