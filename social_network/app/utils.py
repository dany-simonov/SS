import re

def is_valid_image_url(url: str) -> bool:
    """Проверяет валидность URL изображения"""
    if not url:
        return False

    valid_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.webp']
    return any(url.lower().endswith(ext) for ext in valid_extensions)

def extract_image_url(html_response: str) -> str:
    """Извлекает URL изображения из HTML-ответа"""
    url_pattern = r'https://[^\s<>"]+?(?:jpg|jpeg|png|gif|webp)'
    matches = re.findall(url_pattern, html_response)
    return matches[0] if matches else ''