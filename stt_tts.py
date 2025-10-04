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
            # For STT we will launch SpeechRecognizer intent in a separate thread
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
        # Simple loop that uses Android SpeechRecognizer continuously.
        if not ANDROID:
            return
        SpeechRecognizer = autoclass('android.speech.SpeechRecognizer')
        RecognizerIntent = autoclass('android.speech.RecognizerIntent')
        intent = RecognizerIntent()
        intent = RecognizerIntent.ACTION_RECOGNIZE_SPEECH
        # For safety we use basic approach: start activity for result is more robust,
        # but continuous recognition on all devices is inconsistent.
        # So here we simply note: use platform-specific approach in production.
        # This implementation is minimal and may require adjustments.
        # Fallback: do nothing for now.
        pass

    def start_listening(self, callback):
        # callback(text) will be called on recognized text.
        self._callback = callback
        if ANDROID:
            # For robust usage implement SpeechRecognizer with RecognitionListener via pyjnius.
            # Here we spawn a background thread that periodically checks (placeholder).
            t = threading.Thread(target=self._android_listen_loop, daemon=True)
            t.start()
        else:
            # fallback: simulate no STT on desktop
            t = threading.Thread(target=self._desktop_sim, daemon=True)
            t.start()

    def _desktop_sim(self):
        # Just sample input loop for desktop testing (non-blocking)
        while True:
            time.sleep(0.1)
            # nothing by default

    def _android_listen_loop(self):
        # Placeholder: better to implement RecognitionListener via pyjnius.
        # For MVP we will not implement the full listener here.
        # Suggestion: implement in MainActivity native Kotlin or use SpeechRecognizer via Intent.
        return
