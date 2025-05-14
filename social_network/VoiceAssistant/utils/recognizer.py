import os
import json
import pyaudio
import numpy as np
import noisereduce as nr
from vosk import Model, KaldiRecognizer

class SpeechRecognizer:
    def __init__(self, model_path="models/model"):
        if not os.path.exists(model_path):
            raise FileNotFoundError(f"Модель не найдена по пути: {model_path}")
        self.model = Model(model_path)
        self.recognizer = KaldiRecognizer(self.model, 16000)
        self.audio = pyaudio.PyAudio()
        self.stream = self.audio.open(format=pyaudio.paInt16,
                                      channels=1,
                                      rate=16000,
                                      input=True,
                                      frames_per_buffer=4096)
        self.stream.start_stream()

    def recognize_once(self):
        print("[INFO] Прослушивание...")
        frames = []

        while True:
            data = self.stream.read(4096, exception_on_overflow=False)
            frames.append(data)
            if self.recognizer.AcceptWaveform(data):
                break

        print("[INFO] Обработка и фильтрация шума...")
        # Преобразуем в массив для обработки
        audio_data = np.frombuffer(b''.join(frames), dtype=np.int16)
        reduced_noise = nr.reduce_noise(y=audio_data, sr=16000)
        reduced_bytes = reduced_noise.astype(np.int16).tobytes()

        # Распознаем финально
        self.recognizer = KaldiRecognizer(self.model, 16000)
        self.recognizer.AcceptWaveform(reduced_bytes)
        result = json.loads(self.recognizer.Result())
        return result.get("text", "")
