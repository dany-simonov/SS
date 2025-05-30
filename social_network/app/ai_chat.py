from flask import jsonify
import g4f
from social_network.app.utils import extract_image_url

# Текстовые провайдеры
text_providers = [
    g4f.Provider.PollinationsAI,
    g4f.Provider.Qwen_Qwen_2_5M,
    g4f.Provider.Websim,
    g4f.Provider.Free2GPT,
    g4f.Provider.Qwen_Qwen_2_5,
    g4f.Provider.ChatGLM,
    g4f.Provider.GizAI,
    g4f.Provider.Qwen_Qwen_2_72B,
    g4f.Provider.AnyProvider,
    g4f.Provider.FreeGpt
]

# Провайдеры для генерации изображений
image_providers = [
    g4f.Provider.ImageLabs,
    g4f.Provider.BlackForestLabs_Flux1Dev,
    g4f.Provider.PollinationsImage
]

g4f.debug.logging = True
g4f.check_version = False

def handle_ai_chat(request):
    """
    Обрабатывает запросы для AI-чатов и генерации текста или изображений.

    Функция принимает JSON-запрос, содержащий историю диалога, параметры генерации
    и тип запроса (текст или изображение). В зависимости от типа запроса, вызывается
    соответствующий провайдер для генерации ответа.

    Args:
        request (flask.Request): HTTP-запрос, содержащий JSON с данными для обработки.
            Ожидаемые поля:
            - history (list): История диалога (массив объектов с полями "role" и "content").
            - type (str): Тип генерации ('text' или 'image').
            - model (str): Название модели или провайдера (опционально).
            - tone (str): Тон ответа (например, 'friendly').
            - maxLength (int): Максимальная длина ответа в словах.
            - temperature (float): Уровень креативности (от 0 до 1).
            - language (str): Язык ответа ('ru' или 'en').
            - image_provider (str): Провайдер для генерации изображений (опционально).

    Returns:
        flask.Response: JSON-ответ с результатами обработки запроса.
            Возможные поля:
            - success (bool): Успех операции.
            - response (str): Сгенерированный текст или HTML-код изображения.
            - provider (str): Имя использованного провайдера.
            - message (str): Сообщение об ошибке (если успех = False).

    Raises:
        Exception: Если все провайдеры недоступны или возникла ошибка при обработке.
    """
    data = request.get_json()
    history        = data.get('history', [])
    user_message   = history[-1]['content'] if history else ''
    generation_type = data.get('type', 'text')
    selected_model  = data.get('model', text_providers[0].__name__)
    tone         = data.get('tone', 'friendly')
    max_length   = data.get('maxLength', '500')
    temperature  = float(data.get('temperature', 0.5))
    language     = data.get('language', 'ru')

    if not user_message:
        return jsonify({'success': False, 'message': 'Пожалуйста, введите сообщение.'})

    system_prompt = (
        f"Ты — AI-ассистент StudySphere. Тон в котором надо разговаривать: {tone}. "
        f"Длина ответа ≤{max_length} слов. "
        f"Язык: {'English' if language=='en' else 'Русский'}.\n"
        f"Креативность ответа: {temperature} из 1.\n"
        "- Представляться как StudySphere но только в 1 сообщение\n"
        "- Помогать с учебными вопросами\n"
        "- Объяснять простым языком\n"
        "- Давать практические советы\n"
        "- Поддерживать мотивацию\n"
        "- Общаться в дружелюбном тоне\n"
        "- Быть полезным и информативным"
    )

    if generation_type == 'text':
        provider_map = {p.__name__: p for p in text_providers}
        provider = provider_map.get(selected_model, text_providers[0])

        if provider == g4f.Provider.FreeGpt:
            user_message = "Пожалуйста, отвечай на русском: " + user_message

        try:
            msgs = [{"role":"system","content":system_prompt}]
            for item in history:
                msgs.append({"role": item['role'], "content": item['content']})
            response = g4f.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=msgs,
                provider=provider,
                temperature=temperature,
                timeout=120
            )
            return jsonify({
                'success': True,
                'response': response,
                'provider': provider.__name__
            })
        except Exception:
            # fallback
            for p in text_providers:
                if p == provider: continue
                try:
                    msg = user_message
                    if p == g4f.Provider.FreeGpt:
                        msg = "Пожалуйста, отвечай на русском: " + user_message
                    resp = g4f.ChatCompletion.create(
                        model="gpt-3.5-turbo",
                        messages=[
                            {"role": "system", "content": system_prompt},
                            {"role": "user",   "content": msg}
                        ],
                        provider=p,
                        temperature=temperature,
                        timeout=120
                    )
                    return jsonify({
                        'success': True,
                        'response': resp,
                        'provider': p.__name__
                    })
                except:
                    continue
            return jsonify({'success': False, 'message': 'Все текстовые провайдеры недоступны.'})

    else:
        chosen = data.get('image_provider')
        if chosen:
            image_providers.insert(0, getattr(g4f.Provider, chosen, image_providers[0]))
        for p in image_providers:
            try:
                raw = g4f.ChatCompletion.create(
                    model="image-model",
                    messages=[{"role": "user", "content": user_message}],
                    provider=p,
                    timeout=120
                )
                url = extract_image_url(raw)
                if url:
                    html = (
                        '<div class="image-container">'
                        f'<img src="{url}" style="max-width:100%;border-radius:5px">'
                        '</div>'
                    )
                    return jsonify({
                        'success': True,
                        'response': html,
                        'type': 'image',
                        'provider': p.__name__
                    })
            except:
                continue
        return jsonify({'success': False, 'message': 'Не удалось сгенерировать изображение.'})
