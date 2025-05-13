# utils/commands.py
import webbrowser
from utils.ai import AIResponder  # Подключим ИИ-модуль

class CommandProcessor:
    def __init__(self):
        self.ai = AIResponder()

    def process(self, query: str) -> str:
        query = query.lower()

        if query.startswith("найди "):
            search_term = query.replace("найди", "").strip()
            webbrowser.open(f"https://yandex.ru/search/?text={search_term}")
            return f"Ищу в Яндексе: {search_term}"

        if "открой браузер" in query:
            webbrowser.open("https://yandex.ru")
            return "Открываю браузер"

        if "создай файл" in query:
            with open("new_file.txt", "w") as f:
                f.write("Файл создан голосовым помощником")
            return "Создан новый файл"

        if query in ["привет", "здравствуй", "добрый день"]:
            return "Здравствуйте! Чем могу помочь?"

        # Если ничего не подошло — пробуем ИИ
        return self.ai.get_response(query)
