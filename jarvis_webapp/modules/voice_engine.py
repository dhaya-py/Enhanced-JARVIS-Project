"""
Continuous Voice Recognition and Speech Synthesis Module
"""
import pyttsx3
import speech_recognition as sr
import threading
import time
import queue

class VoiceEngine:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.recognizer.energy_threshold = 400
        self.recognizer.dynamic_energy_threshold = True
        
        self.is_listening = False
        self.callback = None
        
        self.speech_queue = queue.Queue()
        # We start the speaker thread to handle pyttsx3
        self.speaker_thread = threading.Thread(target=self._speaker_loop, daemon=True)
        self.speaker_thread.start()

    def set_callback(self, callback):
        self.callback = callback

    def _speaker_loop(self):
        # pyttsx3 init must happen in the thread it will be used in
        # especially on Windows (COM objects)
        tts_engine = pyttsx3.init()
        tts_engine.setProperty('rate', 170)
        tts_engine.setProperty('volume', 0.9)
        while True:
            text = self.speech_queue.get()
            if text is None:
                break
            try:
                tts_engine.say(text)
                tts_engine.runAndWait()
            except Exception as e:
                print(f"[VoiceEngine TTS Error] {e}")

    def speak(self, text):
        if text:
            self.speech_queue.put(text)

    def _listen_loop(self):
        try:
            with sr.Microphone() as source:
                self.recognizer.adjust_for_ambient_noise(source, duration=1)
                print("[VoiceEngine] Listening...")
                while self.is_listening:
                    try:
                        audio = self.recognizer.listen(source, timeout=1, phrase_time_limit=10)
                        text = self.recognizer.recognize_google(audio)
                        if text and self.callback:
                            self.callback(text.lower())
                    except sr.WaitTimeoutError:
                        continue
                    except sr.UnknownValueError:
                        continue
                    except sr.RequestError:
                        time.sleep(2)
                    except Exception as e:
                        print(f"[VoiceEngine Listen Error] {e}")
        except Exception as e:
            print(f"[VoiceEngine Microphone Error] {e}")

    def start_listening(self):
        if self.is_listening:
            return
        self.is_listening = True
        t = threading.Thread(target=self._listen_loop, daemon=True)
        t.start()
        
    def stop_listening(self):
        self.is_listening = False

voice_engine = VoiceEngine()
