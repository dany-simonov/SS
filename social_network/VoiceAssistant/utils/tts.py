import os
import pyttsx3
from uuid import uuid4

class TextToSpeech:
    def __init__(self):
        self.engine = pyttsx3.init()
        self.engine.setProperty('rate', 150)

        # Установка голоса (проверка русских голосов)
        for voice in self.engine.getProperty('voices'):
            if 'russian' in voice.name.lower() or 'рус' in voice.name.lower():
                self.engine.setProperty('voice', voice.id)
                break

        os.makedirs("static/audio", exist_ok=True)

    def speak(self, text, filename=None):
        if not filename:
            filename = f"{uuid4().hex}.mp3"
        filepath = os.path.join("static/audio", filename)

        self.engine.save_to_file(text, filepath)
        self.engine.runAndWait()

        return filename  # Вернём имя файла, чтобы отдать фронту ссылку
