from flask import jsonify
import asyncio
import g4f
from social_network.app.utils import extract_image_url
from social_network.app.enhanced_generation import EnhancedGeneration

text_providers = [
    g4f.Provider.ChatGLM,
    g4f.Provider.Free2GPT,
    g4f.Provider.GizAI
]

image_providers = [
    g4f.Provider.ImageLabs
]

g4f.debug.logging = True
g4f.check_version = False

async def get_enhanced_response(user_message):
    enhanced_gen = EnhancedGeneration()
    return await enhanced_gen.get_response(user_message)

def handle_ai_chat(request):
    data = request.get_json()
    user_message = data.get('message')
    selected_model = data.get('model', 'ChatGLM')
    generation_type = data.get('type', 'text')
    is_enhanced = data.get('enhanced', False)

    if not user_message:
        return jsonify({'success': False, 'message': 'Пожалуйста, введите сообщение.'})

    system_prompt = """Ты - дружелюбный AI-ассистент StudySphere. Твои основные задачи:
                    - Помогать с учебными вопросами по любым предметам
                    - Объяснять сложные темы простым языком  
                    - Давать практические советы по обучению
                    - Поддерживать мотивацию к учёбе
                    - Общаться в дружелюбном тоне
                    - Можешь шутить и поддерживать неформальную беседу
                    - При этом всегда оставаться полезным и информативным."""

    if generation_type == 'text':
        try:
            if is_enhanced:
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                result = loop.run_until_complete(get_enhanced_response(user_message))
                return jsonify(result)
            else:
                provider_map = {
                    'ChatGLM': g4f.Provider.ChatGLM,
                    'Free3GPT': g4f.Provider.Free2GPT,
                    'GizAI': g4f.Provider.GizAI
                }

                provider = provider_map.get(selected_model)
                response = g4f.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_message}
                    ],
                    provider=provider,
                    timeout=120
                )

                return jsonify({'success': True, 'response': response})

        except Exception as e:
            return jsonify({'success': False, 'message': f'Ошибка при использовании {selected_model}'})

    else:
        try:
            image_provider = image_providers[0]
            raw_response = g4f.ChatCompletion.create(
                model="image-model",
                messages=[{"role": "user", "content": user_message}],
                provider=image_provider,
                timeout=120
            )
            image_url = extract_image_url(raw_response)
            if image_url:
                response = (
                    f'<div class="image-container">'
                    f'<img src="{image_url}" style="max-width: 100%; border-radius: 5px;">'
                    f'</div>'
                )
                return jsonify({
                    'success': True,
                    'response': response,
                    'type': 'image'
                })
            else:
                return jsonify({
                    'success': False,
                    'message': 'Не удалось сгенерировать изображение'
                })

        except Exception as e:
            return jsonify({
                'success': False,
                'message': f'Ошибка при генерации изображения: {str(e)}'
            })