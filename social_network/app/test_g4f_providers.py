import g4f
import asyncio
import time
from datetime import datetime
import json

class G4FProviderTester:
    """
    Класс для тестирования провайдеров текста и изображений из библиотеки g4f.

    Этот класс позволяет:
    - Получить список всех доступных провайдеров.
    - Протестировать каждый провайдер на работоспособность.
    - Сохранить результаты тестирования в JSON-файл.
    - Вывести сводку по результатам тестирования.

    Атрибуты:
        results (dict): Словарь с результатами тестирования для текстовых и графических провайдеров.
        test_message (str): Тестовое сообщение для проверки текстовых провайдеров.
        test_image_prompt (str): Тестовый запрос для проверки графических провайдеров.
    """
    def __init__(self):
        """
        Инициализирует экземпляр класса G4FProviderTester.

        Создает структуру для хранения результатов тестирования и задает тестовые сообщения.
        """
        self.results = {
            "text_providers": {},
            "image_providers": {},
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        self.test_message = "Hello, can you respond to this simple test message?"
        self.test_image_prompt = "A beautiful sunset over mountains"
        
    def get_all_providers(self):
        """
        Получает все доступные провайдеры из g4f.

        Returns:
            list: Список классов провайдеров, доступных в g4f.Provider.
        """
        all_providers = []
        for attr_name in dir(g4f.Provider):
            attr = getattr(g4f.Provider, attr_name)
            # Check if it's a provider class (has working attribute)
            if hasattr(attr, 'working') and not attr_name.startswith('__'):
                all_providers.append(attr)
        return all_providers
    
    def test_text_provider(self, provider):
        """
        Тестирует текстового провайдера.

        Args:
            provider: Класс провайдера для тестирования.

        Returns:
            dict: Результат тестирования, включая статус, время отклика и ответ.
        """
        provider_name = provider.__name__
        print(f"Testing text provider: {provider_name}")
        
        start_time = time.time()
        try:
            response = g4f.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": self.test_message}],
                provider=provider,
                timeout=30  # Shorter timeout for testing
            )
            elapsed_time = time.time() - start_time
            
            # Check if response is valid
            if response and isinstance(response, str) and len(response) > 5:
                return {
                    "status": "working",
                    "response_time": round(elapsed_time, 2),
                    "sample": response[:100] + "..." if len(response) > 100 else response
                }
            else:
                return {
                    "status": "invalid_response",
                    "response_time": round(elapsed_time, 2),
                    "error": "Empty or invalid response"
                }
                
        except Exception as e:
            elapsed_time = time.time() - start_time
            return {
                "status": "error",
                "response_time": round(elapsed_time, 2),
                "error": str(e)
            }
    
    def test_image_provider(self, provider):
        """
        Тестирует графического провайдера.

        Args:
            provider: Класс провайдера для тестирования.

        Returns:
            dict: Результат тестирования, включая статус, время отклика и URL изображения.
        """
        provider_name = provider.__name__
        print(f"Testing image provider: {provider_name}")
        
        start_time = time.time()
        try:
            response = g4f.ChatCompletion.create(
                model="image-model",
                messages=[{"role": "user", "content": self.test_image_prompt}],
                provider=provider,
                timeout=60  # Images may take longer
            )
            elapsed_time = time.time() - start_time
            
            # For image providers, we expect a URL or base64 image data
            from social_network.app.utils import extract_image_url
            image_url = extract_image_url(response)
            
            if image_url:
                return {
                    "status": "working",
                    "response_time": round(elapsed_time, 2),
                    "image_url": image_url
                }
            else:
                return {
                    "status": "invalid_response",
                    "response_time": round(elapsed_time, 2),
                    "error": "Could not extract image URL",
                    "raw_response": response[:200] if response else None
                }
                
        except Exception as e:
            elapsed_time = time.time() - start_time
            return {
                "status": "error",
                "response_time": round(elapsed_time, 2),
                "error": str(e)
            }
    
    def run_tests(self):
        """
        Запускает тестирование всех доступных провайдеров.

        Проходит по всем провайдерам, определяет их тип (текст или изображение),
        тестирует их и сохраняет результаты.

        Returns:
            dict: Итоговые результаты тестирования.
        """
        providers = self.get_all_providers()
        
        # Test each provider
        for provider in providers:
            provider_name = provider.__name__
            
            # Skip abstract base classes or non-working providers
            if not hasattr(provider, 'working') or provider_name == 'BaseProvider':
                continue
                
            # Check if it's an image provider
            is_image_provider = False
            for attr_name in dir(provider):
                if attr_name == 'supports_image_generation' and getattr(provider, attr_name):
                    is_image_provider = True
                    break
            
            # Test the provider
            if is_image_provider:
                result = self.test_image_provider(provider)
                self.results["image_providers"][provider_name] = result
            else:
                result = self.test_text_provider(provider)
                self.results["text_providers"][provider_name] = result
        
        return self.results
    
    def save_results(self, filename="g4f_provider_test_results.json"):
        """
        Сохраняет результаты тестирования в JSON-файл.

        Args:
            filename (str): Имя файла для сохранения результатов.
        """
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(self.results, f, indent=2, ensure_ascii=False)
        print(f"Results saved to {filename}")
        
    def print_summary(self):
        """
        Выводит сводку результатов тестирования.

        Показывает количество рабочих и нерабочих провайдеров для текста и изображений.
        """
        working_text = sum(1 for p, r in self.results["text_providers"].items() if r["status"] == "working")
        total_text = len(self.results["text_providers"])
        
        working_image = sum(1 for p, r in self.results["image_providers"].items() if r["status"] == "working")
        total_image = len(self.results["image_providers"])
        
        print("\n===== G4F PROVIDER TEST SUMMARY =====")
        print(f"Text Providers: {working_text}/{total_text} working")
        print(f"Image Providers: {working_image}/{total_image} working")
        print("=====================================\n")
        
        print("Working Text Providers:")
        for provider, result in self.results["text_providers"].items():
            if result["status"] == "working":
                print(f"  - {provider} ({result['response_time']}s)")
        
        print("\nWorking Image Providers:")
        for provider, result in self.results["image_providers"].items():
            if result["status"] == "working":
                print(f"  - {provider} ({result['response_time']}s)")


def main():
    """
    Основная функция для запуска тестирования провайдеров.

    Создает экземпляр G4FProviderTester, запускает тесты, выводит сводку
    и сохраняет результаты в файл.
    """
    print("Starting G4F provider tests...")
    tester = G4FProviderTester()
    tester.run_tests()
    tester.print_summary()
    tester.save_results()
    print("Tests completed!")


if __name__ == "__main__":
    main()
