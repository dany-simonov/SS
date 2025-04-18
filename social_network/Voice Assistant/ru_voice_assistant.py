#python "social_network/Voice Assistant/ru_voice_assistant.py" - для запуска
# LOG (VoskAPI:ReadDataFiles():model.cc:323) Loading RNNLM model from C:/Users/redmi/Desktop/SS/social_network/Voice Assistant/model/rnnlm/final.raw
# после этого лога начинает слушать

# Скрипт, который по голосовой команде "напиши что-то"
# пишет сказанный текст в любом поле ввода, в любой программе
# а по команде "найди что-то" открывает поиск

from vosk import Model, KaldiRecognizer
import pyaudio
import pyperclip
# Модуль для работы с клавиатурой
import keyboard
# Модкль для создания пауз в работе программы
import time
# Модуль для работы с json
import json
# Модуль для открытия браузера
import webbrowser  
# Ключевые слова фразу после которых нужно напечатать
flags = ['напиши','напечатаю','напечатает','напечатайте','напечатать', 'напечатай', 'введи текст', 'ввести текст']
# Ключевые слова фразу после которых нужно найти в сети
flags2 = ['найти', 'найди', 'поиск', 'поищи', 'искать']
# загружаем модель распознавания речи
model = Model("C:/Users/redmi/Desktop/SS/social_network/Voice Assistant/model")
# Объявляем распознаватель речи и его частоту дискретизации звука
rec = KaldiRecognizer(model, 16000)
# Слушаем звук с микрофона
p = pyaudio.PyAudio()
stream = p.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=8000)
stream.start_stream()

# Функция ищет есть ли в сказанной фразе ключевые слова из списка flags
def isflag(txt, xflags):
    # Проходим по списку ключевых слов
    for flagword in xflags:
        # Если ключевое слово есть во фразе
        if flagword in txt:
            # Возвращаем это слово
            return flagword

# Функция которая вставляет текст в любое поле любого окна
def pastetxt(txt):
    # Сперва мы копируем содержимое буфера обмена в переменную
    # чтобы не потерять если что-то было скопировано
    buffer = pyperclip.paste()
    # Теперь мы копируем в буфер обмена наш сказанный текст
    pyperclip.copy(txt.capitalize() + '. ')
    # Делаем паузу
    time.sleep(0.7)
    # Эмулируем нажатие клавиш для вставки скопированного
    keyboard.press_and_release('ctrl + v')
    # Снова пауза
    time.sleep(0.5)
    # Возвращаем в буфер обмена то что в нём было ранее
    pyperclip.copy(buffer)

# Функция которая открывает поиск в браузере с соответствующим запросом
def findtxt(txt):
    webbrowser.open('https://google.com/search?q=' + txt.replace(' ', '+'))

# Ожидаем голосовых команд 
while True:
    # Получаем с микрофона порцию звука
    data = stream.read(4000, exception_on_overflow=False)
    if len(data) == 0:
        continue
    # Если что-то распозналось
    if rec.AcceptWaveform(data):
        # Получаем распознанный текст
        txt = json.loads(rec.Result())["text"]
        # Если он не пустой
        if txt.strip() != '':
            # Печатаем его на экране
            print('Вы сказали: ', txt)
            # Ищем ключевые слова
            flagword = isflag(txt, flags)
            # Если они найдены
            if flagword != None:
                # Очищаем сказанный текст от ключевых слов
                txt = txt.replace(flagword, '').strip()
                # и вставляем его в текущее активное поле ввода
                pastetxt(txt)
            # Ищем ключевые слова
            flagword2 = isflag(txt, flags2)
            # Если они найдены
            if flagword2 != None:
                # Очищаем сказанный текст от ключевых слов
                txt = txt.replace(flagword2, '').strip()
                # ищем сказанный текст в гугле
                findtxt(txt)

