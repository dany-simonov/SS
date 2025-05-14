# utils/ai.py
import requests
from typing import Optional

class AIResponder:
    """
    Класс для взаимодействия с AI-сервисом вашего приложения.
    Отправляет запросы на Flask-эндпоинт и возвращает текстовые ответы.
    """
    def __init__(self,
                 base_url: str = "http://localhost:5000/ai-chat/ai-chat",
                 default_model: str = "ChatGLM",
                 timeout: int = 120):
        self.base_url = base_url.rstrip('/')
        self.default_model = default_model
        self.timeout = timeout

    def get_response(self,
                     prompt: str,
                     model: Optional[str] = None,
                     enhanced: bool = False) -> str:
        """
        Отправляет запрос в AI-сервис и возвращает текстовый ответ.

        :param prompt: Текст запроса пользователя.
        :param model: Имя модели из text_providers (ChatGLM, Free2GPT, GizAI).
        :param enhanced: Если True, используется расширенная генерация через EnhancedGeneration.
        :return: Ответ AI в формате строки.
        """
        url = self.base_url
        payload = {
            "message": prompt,
            "model": model or self.default_model,
            "type": "text",
            "enhanced": enhanced
        }
        try:
            resp = requests.post(url, json=payload, timeout=self.timeout)
            resp.raise_for_status()
            data = resp.json()

            if not data.get("success", True):
                return f"(ИИ ошибка): {data.get('message', 'Неизвестная ошибка')}"

            # В некоторых реализациях ответ может быть в поле 'response'
            response = data.get("response")
            if response is None:
                return "(ИИ): получен пустой ответ"
            return response

        except requests.exceptions.RequestException as e:
            return f"(Сетевая ошибка ИИ): {str(e)}"
