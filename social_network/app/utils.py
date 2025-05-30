import re

def is_valid_image_url(url: str) -> bool:
    """
    Проверяет, является ли переданный URL валидным URL изображения.

    Аргументы:
        url (str): Строка, представляющая URL для проверки.

    Возвращает:
        bool: True, если URL заканчивается на допустимое расширение изображения
              (.jpg, .jpeg, .png, .gif, .webp), иначе False.
    """
    if not url:
        return False

    valid_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.webp']
    return any(url.lower().endswith(ext) for ext in valid_extensions)

def extract_image_url(html_response: str) -> str:
    """
    Извлекает первый URL изображения из HTML-ответа.

    Функция ищет URL, начинающийся с 'https://'  и заканчивающийся на одно из допустимых
    расширений изображений (.jpg, .jpeg, .png, .gif, .webp).

    Аргументы:
        html_response (str): Строка, содержащая HTML-код для анализа.

    Возвращает:
        str: Первый найденный URL изображения, если он существует, иначе пустая строка.
    """
    url_pattern = r'https://[^\s<>"]+?(?:jpg|jpeg|png|gif|webp)'
    matches = re.findall(url_pattern, html_response)
    return matches[0] if matches else ''