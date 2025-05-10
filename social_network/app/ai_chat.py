# from flask import jsonify
# import asyncio
# import g4f
# from social_network.app.utils import extract_image_url
# from .enhanced_generation import EnhancedGeneration

# # Текстовые провайдеры в порядке приоритета
# text_providers = [
#     g4f.Provider.Qwen_Qwen_2_5M,
#     g4f.Provider.PollinationsAI,
#     g4f.Provider.Websim,
#     g4f.Provider.Free2GPT,
#     g4f.Provider.Qwen_Qwen_2_5,
#     g4f.Provider.ChatGLM,
#     g4f.Provider.GizAI,
#     g4f.Provider.Qwen_Qwen_2_72B,
#     g4f.Provider.AnyProvider,
#     g4f.Provider.FreeGpt
# ]

# # Провайдеры для генерации изображений в порядке приоритета
# image_providers = [
#     g4f.Provider.PollinationsImage,
#     g4f.Provider.ImageLabs,
#     g4f.Provider.BlackForestLabs_Flux1Dev
# ]

# g4f.debug.logging = True
# g4f.check_version = False

# async def get_enhanced_response(user_message):
#     enhanced_gen = EnhancedGeneration()
#     return await enhanced_gen.get_response(user_message)

# def handle_ai_chat(request):
#     data = request.get_json()
#     user_message = data.get('message')
#     selected_model = data.get('model', 'Qwen_Qwen_2_5M')
#     generation_type = data.get('type', 'text')
#     is_enhanced = data.get('enhanced', False)

#     if not user_message:
#         return jsonify({'success': False, 'message': 'Пожалуйста, введите сообщение.'})

#     system_prompt = """Ты - дружелюбный AI-ассистент StudySphere. Твои основные задачи:
#                     - Представляйся как StudySphere!
#                     - Помогать с учебными вопросами по любым предметам
#                     - Объяснять сложные темы простым языком  
#                     - Давать практические советы по обучению
#                     - Поддерживать мотивацию к учёбе
#                     - Общаться в дружелюбном тоне
#                     - Можешь шутить и поддерживать неформальную беседу
#                     - При этом всегда оставаться полезным и информативным."""

#     if generation_type == 'text':
#         try:
#             if is_enhanced:
#                 loop = asyncio.new_event_loop()
#                 asyncio.set_event_loop(loop)
#                 result = loop.run_until_complete(get_enhanced_response(user_message))
#                 return jsonify(result)
#             else:
#                 # Создаем словарь всех текстовых провайдеров
#                 provider_map = {
#                     'Qwen_Qwen_2_5M': g4f.Provider.Qwen_Qwen_2_5M,
#                     'PollinationsAI': g4f.Provider.PollinationsAI,
#                     'Websim': g4f.Provider.Websim,
#                     'Free2GPT': g4f.Provider.Free2GPT,
#                     'Qwen_Qwen_2_5': g4f.Provider.Qwen_Qwen_2_5,
#                     'GizAI': g4f.Provider.GizAI,
#                     'Qwen_Qwen_2_72B': g4f.Provider.Qwen_Qwen_2_72B,
#                     'AnyProvider': g4f.Provider.AnyProvider,
#                     'FreeGpt': g4f.Provider.FreeGpt
#                 }
                
#                 # Получаем провайдера из словаря или используем первый в списке по умолчанию
#                 provider = provider_map.get(selected_model, text_providers[0])
                
#                 # Если выбран FreeGpt, добавляем инструкцию по языку
#                 if selected_model == 'FreeGpt':
#                     user_message = "Пожалуйста, ответь на русском языке: " + user_message
                
#                 response = g4f.ChatCompletion.create(
#                     model="gpt-3.5-turbo",
#                     messages=[
#                         {"role": "system", "content": system_prompt},
#                         {"role": "user", "content": user_message}
#                     ],
#                     provider=provider,
#                     timeout=120
#                 )
#                 return jsonify({'success': True, 'response': response})
#         except Exception as e:
#             # Пробуем использовать следующего провайдера в списке
#             for provider in text_providers:
#                 try:
#                     provider_name = provider.__name__
#                     # Пропускаем текущий провайдер, который уже вызвал ошибку
#                     if provider_name == selected_model:
#                         continue
                    
#                     # Если используем FreeGpt, добавляем инструкцию по языку
#                     current_message = user_message
#                     if provider == g4f.Provider.FreeGpt:
#                         current_message = "Пожалуйста, ответь на русском языке: " + user_message
                    
#                     response = g4f.ChatCompletion.create(
#                         model="gpt-3.5-turbo",
#                         messages=[
#                             {"role": "system", "content": system_prompt},
#                             {"role": "user", "content": current_message}
#                         ],
#                         provider=provider,
#                         timeout=120
#                     )
#                     return jsonify({
#                         'success': True, 
#                         'response': response,
#                         'fallback_provider': provider_name
#                     })
#                 except:
#                     continue
            
#             # Если все провайдеры не сработали
#             return jsonify({
#                 'success': False, 
#                 'message': f'Не удалось получить ответ. Все провайдеры перегруженны.'
#             })
#     else:  # Для генерации изображений
#         # Пробуем каждый провайдер изображений по очереди
#         for image_provider in image_providers:
#             try:
#                 raw_response = g4f.ChatCompletion.create(
#                     model="image-model",
#                     messages=[{"role": "user", "content": user_message}],
#                     provider=image_provider,
#                     timeout=120
#                 )
#                 image_url = extract_image_url(raw_response)
#                 if image_url:
#                     response = (
#                         f'<div class="image-container">'
#                         f'<img src="{image_url}" style="max-width: 100%; border-radius: 5px;">'
#                         f'</div>'
#                     )
#                     return jsonify({
#                         'success': True,
#                         'response': response,
#                         'type': 'image',
#                         'provider': image_provider.__name__
#                     })
#             except Exception:
#                 continue
        
#         # Если все провайдеры изображений не сработали
#         return jsonify({
#             'success': False,
#             'message': 'Не удалось сгенерировать изображение. Все провайдеры перегруженны.'
#         })

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
    g4f.Provider.PollinationsImage,
    g4f.Provider.ImageLabs,
    g4f.Provider.BlackForestLabs_Flux1Dev
]

g4f.debug.logging = True
g4f.check_version = False

def handle_ai_chat(request):
    data = request.get_json()
    user_message   = data.get('message')
    generation_type = data.get('type', 'text')
    selected_model = data.get('model', text_providers[0].__name__)

    if not user_message:
        return jsonify({'success': False, 'message': 'Пожалуйста, введите сообщение.'})

    system_prompt = (
        "Ты — дружелюбный AI-ассистент StudySphere. Твои задачи:\n"
        "- Представляться как StudySphere\n"
        "- Помогать с учебными вопросами\n"
        "- Объяснять простым языком\n"
        "- Давать практические советы\n"
        "- Поддерживать мотивацию\n"
        "- Общаться в дружелюбном тоне\n"
        "- Быть полезным и информативным"
    )

    if generation_type == 'text':
        # TEXT
        # собираем карту провайдеров
        provider_map = {p.__name__: p for p in text_providers}
        provider = provider_map.get(selected_model, text_providers[0])

        # если выбрали FreeGpt — добавляем инструкцию по языку
        if provider == g4f.Provider.FreeGpt:
            user_message = "Пожалуйста, отвечай на русском: " + user_message

        try:
            response = g4f.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user",   "content": user_message}
                ],
                provider=provider,
                timeout=120
            )
            return jsonify({'success': True, 'response': response, 'provider': provider.__name__})
        except Exception:
            # fallback на следующих провайдеров
            for p in text_providers:
                if p == provider: 
                    continue
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
                        timeout=120
                    )
                    return jsonify({'success': True, 'response': resp, 'provider': p.__name__})
                except:
                    continue
            return jsonify({'success': False, 'message': 'Все текстовые провайдеры недоступны.'})

    else:
        # IMAGE
        # позволяем пользователю выбрать провайдера через поля JSON
        # (если передали в data["image_provider"], иначе пробуем все)
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
                    html = f'<div class="image-container"><img src="{url}" style="max-width:100%;border-radius:5px"></div>'
                    return jsonify({'success': True, 'response': html, 'type': 'image', 'provider': p.__name__})
            except:
                continue
        return jsonify({'success': False, 'message': 'Не удалось сгенерировать изображение.'})
