from utils.recognizer import SpeechRecognizer
from utils.commands import CommandProcessor
from utils.tts import TextToSpeech
from utils.history import SessionHistory

class AssistantCore:
    def __init__(self):
        self.recognizer = SpeechRecognizer()
        self.commands = CommandProcessor()
        self.tts = TextToSpeech()
        self.history = SessionHistory()

    def listen_and_respond(self):
        query = self.recognizer.recognize_once()
        if not query:
            return None, None

        print(f"[USER]: {query}")
        self.history.add_message("user", query)

        response = self.commands.process(query)
        self.history.add_message("assistant", response)

        audio_filename = self.tts.speak(response)
        return response, audio_filename

    def get_history(self):
        return self.history.get_history()

    def reset_history(self):
        self.history.clear()
