# import g4f
# import asyncio
# from concurrent.futures import ThreadPoolExecutor
# from typing import Optional, List, Dict

# class EnhancedGeneration:
#     def __init__(self, timeout: int = 15):
#         self.timeout = timeout
#         self.providers = {
#             'ChatGLM': g4f.Provider.ChatGLM,
#             'GizAI': g4f.Provider.GizAI,
#             'Free2GPT': g4f.Provider.Free2GPT
#         }
        
#     async def get_response(self, user_message: str) -> Dict:
#         """Main method to handle enhanced generation"""
#         try:
#             # Start parallel analysis and generation
#             analysis_task = self._get_analysis(user_message)
#             generation_task = self._get_generation(user_message)
            
#             # Wait for both tasks with timeout
#             results = await asyncio.gather(
#                 analysis_task,
#                 generation_task,
#                 return_exceptions=True
#             )
            
#             # Process results
#             analysis, generation = results
#             if isinstance(analysis, Exception) and isinstance(generation, Exception):
#                 return {'success': False, 'message': 'Все модели недоступны'}
                
#             # Get final response from Free2GPT
#             final_response = await self._get_final_response(analysis, generation, user_message)
#             return {'success': True, 'response': final_response}
            
#         except Exception as e:
#             return {'success': False, 'message': f'Ошибка улучшенной генерации: {str(e)}'}

#     async def _get_analysis(self, message: str) -> Optional[str]:
#         """Get analysis from ChatGLM"""
#         chatglm_prompt = """Ты - аналитический модуль нейросетевого чат-бота. Твоя задача - получить запрос от пользователя и предоставить максимально полный и точный анализ этого запроса.

#             1.  Получи запрос от пользователя.
#             2.  Тщательно проанализируй запрос, выдели ключевые темы, вопросы и намерения пользователя.
#             3.  Предоставь детальное описание запроса, включая:
#                 *   Ключевые слова и фразы.
#                 *   Общую тему запроса.
#                 *   Возможные вопросы, которые пользователь хочет получить в ответе.
#                 *   Любую другую информацию, которая может быть полезна для генерации ответа.
#             4.  Твой ответ должен быть представлен в формате структурированного текста, который легко понять другой нейросети (GizAI).
#             5.  Отправь свой анализ запроса модулю GizAI.
#             6.  Если в течение 15 секунд ты не сможешь предоставить анализ запроса, сообщи об этом и прекрати работу."""
        
#         try:
#             response = await self._call_provider(
#                 'ChatGLM',
#                 messages=[
#                     {"role": "system", "content": chatglm_prompt},
#                     {"role": "user", "content": message}
#                 ]
#             )
#             return response
#         except Exception:
#             return None

#     async def _get_generation(self, message: str) -> Optional[str]:
#         """Получение ответа от GizAI"""
#         gizai_prompt = """Ты - экспертный модуль нейросетевого чат-бота, отвечающий за генерацию информации. 
#                           Твоя задача - получить анализ запроса от модуля ChatGLM и предоставить максимально точный и полезный ответ на этот запрос.

#             1.  Получи анализ запроса от модуля ChatGLM.
#             2.  Тщательно изучи анализ запроса, чтобы понять ключевые темы, вопросы и намерения пользователя.
#             3.  Используя свои знания и возможности, сгенерируй максимально полный, точный и полезный ответ на запрос пользователя.
#             4.  Твой ответ должен быть представлен в формате структурированного текста, который легко понять другой нейросети (Free2GPT).
#             5.  Отправь свой ответ модулю Free2GPT.
#             6.  Если в течение 15 секунд ты не получишь анализ запроса от модуля ChatGLM или не сможешь сгенерировать ответ, сообщи об этом и прекрати работу.
#             7.  Если ты получил анализ запроса от ChatGLM, но не уверен в своем ответе, попроси ChatGLM уточнить анализ запроса.
#             8.  Если ты и ChatGLM предоставили ответы, проанализируйте ответы друг друга. Цель - убедиться, что ответы полные и точные, а также исключить противоречия. Если вы обнаружили что-то неверное, перефразируйте свой ответ.
#             9.  Общая задача - составить 1 финальный доработанный ответ для пользователя."""
                    
#         try:
#             response = await self._call_provider(
#                 'GizAI',
#                 messages=[
#                     {"role": "system", "content": gizai_prompt},
#                     {"role": "user", "content": message}
#                 ]
#             )
#             return response
#         except Exception:
#             return None

#     async def _get_final_response(self, analysis: Optional[str], 
#                                 generation: Optional[str], 
#                                 original_message: str) -> str:
#         """Формирование финального ответа через Free2GPT"""
        
#         free2gpt_prompt = f"""Ты - дружелюбный и общительный модуль нейросетевого чат-бота, отвечающий за общение с пользователем. 
#                               Твоя задача - получить ответы от модулей ChatGLM и GizAI и представить их пользователю в понятном, дружелюбном и красиво оформленном виде.
#         Анализ запроса: {analysis if analysis else 'недоступен'}
#         Сгенерированный ответ: {generation if generation else 'недоступен'}
        
#             Алгоритм работы:

#             1.  **Получение и анализ:**
#                 *   Получи ответы от модулей ChatGLM и GizAI.
#                 *   Тщательно изучи ответы, чтобы полностью понять их содержание, структуру и смысл. Особое внимание удели выделению ключевых понятий, определений и преимуществ, которые будут интересны пользователю.
#             2.  **Приветствие:**
#                 *   Сформулируй приветствие для пользователя, выразив готовность предоставить информацию о запрошенной теме.
#             3.  **Форматирование ответа:**
#                 *   Представь ответы пользователю в понятной и дружелюбной форме, используя простой и понятный язык, избегая сложных технических терминов, если это возможно.
#                 *   **Обязательно** структурируй ответ, используя следующие элементы:
#                     *   Заголовки 
#                     *   Подзаголовки (для более детального разделения информации).
#                     *   Списки (маркированные или нумерованные) для перечисления ключевых пунктов, преимуществ, особенностей и т.д.
#                     *   Абзацы (для разделения больших блоков текста на более короткие и удобочитаемые).
#                     *   **Используй отступы** для визуального выделения структуры ответа и улучшения его читаемости.
#                 *   **Убери все лишние символы**, такие как:
#                     *   Символы форматирования Markdown (например, *, **, ###, --- и т.д.).
#                     *   Любые другие символы, которые не несут смысловой нагрузки и ухудшают внешний вид ответа.
#                 *   **Сделай акцент на простоту и понятность:** представляй информацию таким образом, чтобы она была легко усваиваемой даже для пользователей, не имеющих опыта в программировании. Используй примеры и аналогии, чтобы объяснить сложные концепции.
#             4.  **Обработка ошибок и противоречий:**
#                 *   Если от одного из модулей (ChatGLM или GizAI) не поступил ответ в течение 15 секунд, возьми ответ от того, кто ответил.
#                 *   Если ответы от модулей ChatGLM и GizAI противоречат друг другу, сообщи об этом пользователю и предложи ему уточнить свой запрос.
#             5.  **Завершение:**
#                 *   В конце ответа поблагодари пользователя за вопрос и предложи ему задать другие вопросы.
#             6.  **Важные правила:**
#                 *   **Не генерируй информацию самостоятельно!** Твоя главная задача - представить информацию, полученную от других модулей, в наилучшем виде.
#                 *   **Не пиши, что ты проанализировал ответы ChatGLM и GizAI!** Говори просто "Я", как если бы ты был обычным человеком."""

#         try:
#             response = await self._call_provider(
#                 'Free2GPT',
#                 messages=[
#                     {"role": "system", "content": free2gpt_prompt},
#                     {"role": "user", "content": original_message}
#                 ]
#             )
#             return response
#         except Exception:
#             # Возвращаем лучший доступный ответ
#             return generation or analysis or "Извините, сервис временно недоступен"

#     async def _call_provider(self, provider: str, messages: List[Dict]) -> str:
#         """Вызов провайдера с таймаутом"""
#         with ThreadPoolExecutor() as executor:
#             try:
#                 future = executor.submit(
#                     g4f.ChatCompletion.create,
#                     model="gpt-3.5-turbo",
#                     provider=self.providers[provider],
#                     messages=messages,
#                     timeout=self.timeout
#                 )
#                 return await asyncio.wrap_future(future)
#             except Exception as e:
#                 print(f"Ошибка провайдера {provider}: {str(e)}")
#                 raise