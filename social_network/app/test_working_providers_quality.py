import g4f
import asyncio
import time
from datetime import datetime
import json
import os
from tabulate import tabulate

class WorkingProvidersTester:
    """
    Класс для тестирования работоспособности и качества ответов провайдеров из библиотеки g4f.

    Этот класс позволяет:
    - Протестировать список заранее отсортированных провайдеров.
    - Оценить качество их ответов по заданным критериям.
    - Сохранить результаты тестирования в файлы для дальнейшего анализа.

    Атрибуты:
        results (dict): Словарь с результатами тестирования для каждого провайдера.
        timestamp (str): Временная метка начала тестирования.
        working_providers (list): Список работающих провайдеров, отсортированный по скорости.
        test_question (str): Сложный вопрос для тестирования провайдеров.
        quality_criteria (list): Критерии оценки качества ответа.
    """
    def __init__(self):
        """
        Инициализирует экземпляр класса WorkingProvidersTester.

        Создает структуру для хранения результатов тестирования, задает тестовый вопрос,
        критерии оценки и создает директории для сохранения результатов.
        """
        self.results = {
            "providers": {},
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        # Список работающих провайдеров, отсортированный по скорости
        self.working_providers = [
            {"name": "Websim", "provider": g4f.Provider.Websim},
            {"name": "PollinationsAI", "provider": g4f.Provider.PollinationsAI},
            {"name": "GizAI", "provider": g4f.Provider.GizAI},
            {"name": "ChatGLM", "provider": g4f.Provider.ChatGLM},
            {"name": "FreeGpt", "provider": g4f.Provider.FreeGpt},
            {"name": "Qwen_Qwen_2_5", "provider": g4f.Provider.Qwen_Qwen_2_5},
            {"name": "Qwen_Qwen_2_5M", "provider": g4f.Provider.Qwen_Qwen_2_5M},
            {"name": "PollinationsImage", "provider": g4f.Provider.PollinationsImage},
            {"name": "HarProvider", "provider": g4f.Provider.HarProvider},
            {"name": "Free2GPT", "provider": g4f.Provider.Free2GPT},
            {"name": "Qwen_Qwen_2_72B", "provider": g4f.Provider.Qwen_Qwen_2_72B},
            {"name": "ImageLabs", "provider": g4f.Provider.ImageLabs},
            {"name": "BlackForestLabs_Flux1Dev", "provider": g4f.Provider.BlackForestLabs_Flux1Dev},
            {"name": "AnyProvider", "provider": g4f.Provider.AnyProvider},
        ]
        
        # Сложный вопрос для тестирования
        self.test_question = """
        Объясни концепцию квантовой запутанности и как она используется в квантовых вычислениях. 
        Также опиши эксперимент Эйнштейна-Подольского-Розена и его значение для понимания квантовой механики.
        Приведи математическое описание и практические примеры применения.
        """
        
        # Критерии оценки качества ответа (от 1 до 10)
        self.quality_criteria = [
            "Точность информации",
            "Полнота ответа",
            "Структурированность",
            "Понятность объяснения",
            "Наличие примеров"
        ]
        
        # Создаем основную директорию для анализа
        os.makedirs("working_providers_analysis", exist_ok=True)
        os.makedirs("working_providers_analysis/responses", exist_ok=True)
        
    def evaluate_response_quality(self, response):
        """
        Автоматическая оценка качества ответа по заданным критериям.

        Args:
            response (str): Ответ провайдера, который нужно оценить.

        Returns:
            dict: Словарь с оценками по каждому критерию и общим баллом.
        """
        evaluation = {}
        
        # Точность информации (проверяем наличие ключевых терминов)
        key_terms = ["квантовая запутанность", "эксперимент ЭПР", "квантовые вычисления", 
                     "суперпозиция", "запутанные состояния", "нелокальность"]
        accuracy_score = sum(1 for term in key_terms if term.lower() in response.lower()) / len(key_terms) * 10
        evaluation["Точность информации"] = round(accuracy_score, 1)
        
        # Полнота ответа (проверяем длину и наличие разделов)
        completeness_score = min(len(response) / 1000, 1) * 10  # Максимум за 1000+ символов
        evaluation["Полнота ответа"] = round(completeness_score, 1)
        
        # Структурированность (проверяем наличие абзацев, заголовков)
        paragraphs = response.count('\n\n')
        structure_score = min(paragraphs / 5, 1) * 10  # Максимум за 5+ абзацев
        evaluation["Структурированность"] = round(structure_score, 1)
        
        # Понятность объяснения (эвристика: соотношение простых и сложных слов)
        words = response.split()
        long_words = sum(1 for word in words if len(word) > 8)
        clarity_score = (1 - min(long_words / len(words) * 3, 0.7)) * 10  # Штраф за слишком много сложных слов
        evaluation["Понятность объяснения"] = round(clarity_score, 1)
        
        # Наличие примеров
        example_indicators = ["например", "пример", "иллюстрация", "case", "применение"]
        examples_score = min(sum(1 for ind in example_indicators if ind.lower() in response.lower()) * 2, 10)
        evaluation["Наличие примеров"] = round(examples_score, 1)
        
        # Общий балл - среднее по всем критериям
        evaluation["Общий балл"] = round(sum(evaluation.values()) / len(evaluation) - 1, 1)
        
        return evaluation
    
    def test_provider(self, provider_info):
        """
        Тестирует одного провайдера.

        Args:
            provider_info (dict): Информация о провайдере, включая имя и класс.

        Returns:
            dict: Результат тестирования, включая статус, время отклика, длину ответа,
                  оценку качества и сам ответ.
        """
        provider_name = provider_info["name"]
        provider = provider_info["provider"]
        
        print(f"Тестирование провайдера: {provider_name}")
        
        start_time = time.time()
        try:
            response = g4f.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": self.test_question}],
                provider=provider,
                timeout=120  # Увеличенный таймаут для сложного вопроса
            )
            elapsed_time = time.time() - start_time
            
            # Проверка валидности ответа
            if response and isinstance(response, str) and len(response) > 50:
                # Оценка качества ответа
                quality_evaluation = self.evaluate_response_quality(response)
                
                return {
                    "status": "working",
                    "response_time": round(elapsed_time, 2),
                    "response_length": len(response),
                    "quality_evaluation": quality_evaluation,
                    "response": response
                }
            else:
                return {
                    "status": "invalid_response",
                    "response_time": round(elapsed_time, 2),
                    "error": "Пустой или недостаточный ответ",
                    "response": response if response else "Нет ответа"
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
        Запускает тесты для всех работающих провайдеров.

        Для каждого провайдера из списка `working_providers` вызывается метод `test_provider`,
        результаты сохраняются в словарь `results`.

        Returns:
            dict: Словарь с результатами тестирования для каждого провайдера.
        """
        for provider_info in self.working_providers:
            provider_name = provider_info["name"]
            result = self.test_provider(provider_info)
            self.results["providers"][provider_name] = result
        
        return self.results
    
    def save_results(self):
        """
        Сохраняет результаты тестирования в JSON-файл и отдельные файлы с ответами провайдеров.

        - Основные результаты сохраняются в файл `quality_test_results.json`.
        - Ответы каждого работающего провайдера сохраняются в отдельные текстовые файлы.
        """
        filename = "working_providers_analysis/quality_test_results.json"
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(self.results, f, indent=2, ensure_ascii=False)
        print(f"Результаты сохранены в {filename}")
        
        # Сохранение ответов каждого провайдера в отдельные файлы
        for provider_name, result in self.results["providers"].items():
            if result["status"] == "working" and "response" in result:
                response_file = f"working_providers_analysis/responses/{provider_name}_response.txt"
                with open(response_file, 'w', encoding='utf-8') as f:
                    f.write(result["response"])
                print(f"Ответ провайдера {provider_name} сохранен в {response_file}")
    
    def generate_report(self):
        """
        Генерирует отчет о тестировании провайдеров в формате Markdown.

        Отчет включает:
        - Дату тестирования.
        - Тестовый вопрос.
        - Сводную таблицу с результатами (статус, время отклика, длина ответа, общий балл).
        - Детальную оценку по каждому критерию качества.
        - Рекомендации по выбору оптимальных провайдеров.

        Результат сохраняется в файл `quality_report.md`.

        Returns:
            str: Сгенерированный отчет в формате Markdown.
        """
        report = "# Отчет о тестировании провайдеров g4f\n\n"
        report += f"Дата тестирования: {self.results['timestamp']}\n\n"
        report += f"## Тестовый вопрос\n\n{self.test_question}\n\n"
        
        # Таблица с результатами
        table_data = []
        headers = ["Провайдер", "Статус", "Время (сек)", "Длина ответа", "Общий балл"]
        
        # Сортировка провайдеров по общему баллу (если есть)
        sorted_providers = []
        for provider_name, result in self.results["providers"].items():
            if result["status"] == "working" and "quality_evaluation" in result:
                sorted_providers.append({
                    "name": provider_name,
                    "result": result,
                    "score": result["quality_evaluation"]["Общий балл"]
                })
        
        # Сортировка по убыванию оценки
        sorted_providers.sort(key=lambda x: x["score"], reverse=True)
        
        # Заполнение таблицы
        for provider_info in sorted_providers:
            provider_name = provider_info["name"]
            result = provider_info["result"]
            row = [
                provider_name,
                "✅ Работает",
                result["response_time"],
                result["response_length"],
                result["quality_evaluation"]["Общий балл"]
            ]
            table_data.append(row)
        
        # Добавление неработающих провайдеров
        for provider_name, result in self.results["providers"].items():
            if result["status"] != "working":
                error_msg = result.get("error", "Неизвестная ошибка")
                row = [
                    provider_name,
                    f"❌ Ошибка: {error_msg[:30]}...",
                    result.get("response_time", "-"),
                    "-",
                    "-"
                ]
                table_data.append(row)
        
        # Добавление таблицы в отчет
        report += "## Сводная таблица результатов\n\n"
        report += tabulate(table_data, headers=headers, tablefmt="pipe") + "\n\n"
        
        # Детальная информация по критериям для работающих провайдеров
        report += "## Детальная оценка по критериям\n\n"
        criteria_table = []
        criteria_headers = ["Провайдер"] + self.quality_criteria
        
        for provider_info in sorted_providers:
            provider_name = provider_info["name"]
            evaluation = provider_info["result"]["quality_evaluation"]
            row = [provider_name]
            for criterion in self.quality_criteria:
                row.append(evaluation[criterion])
            criteria_table.append(row)
        
        report += tabulate(criteria_table, headers=criteria_headers, tablefmt="pipe") + "\n\n"
        
        # Рекомендации
        report += "## Рекомендации\n\n"
        
        if sorted_providers:
            best_provider = sorted_providers[0]["name"]
            fastest_provider = min(
                [p for p in self.results["providers"].items() if p[1]["status"] == "working"],
                key=lambda x: x[1]["response_time"]
            )[0]
            
            report += f"- **Лучшее качество ответов**: {best_provider}\n"
            report += f"- **Самый быстрый провайдер**: {fastest_provider}\n\n"
        
        report += "### Оптимальные провайдеры по категориям:\n\n"
        
        # Находим лучших по каждому критерию
        for criterion in self.quality_criteria:
            if sorted_providers:
                best_for_criterion = max(
                    sorted_providers,
                    key=lambda x: x["result"]["quality_evaluation"][criterion]
                )
                report += f"- **{criterion}**: {best_for_criterion['name']} (оценка: {best_for_criterion['result']['quality_evaluation'][criterion]})\n"
        
        # Сохранение отчета
        report_path = "working_providers_analysis/quality_report.md"
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(report)
        print(f"Отчет сохранен в {report_path}")
        
        return report


def main():
    """
    Основная функция для запуска тестирования провайдеров.

    Создает экземпляр класса `WorkingProvidersTester`, запускает тестирование,
    сохраняет результаты и генерирует отчет.
    """
    print("Начинаем тестирование качества ответов работающих провайдеров g4f...")
    tester = WorkingProvidersTester()
    tester.run_tests()
    tester.save_results()
    tester.generate_report()
    print("Тестирование завершено!")


if __name__ == "__main__":
    main()