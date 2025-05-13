import os
import requests
import zipfile
import sys

DROPBOX_URL = (
    "https://www.dropbox.com/scl/fi/m6ff4lir5wnw054mnx8df/"
    "vosk-model-ru-0.22.zip?rlkey=zrfnc9hvb433sa75jdnyxyw7z&dl=1"
)


def download_model(model_dir="models/model", zip_name="model.zip"):
    """
    Скачивает и распаковывает модель Vosk из Dropbox.
    Если модель уже загружена, не делает ничего.

    :param model_dir: директория для распакованной модели
    :param zip_name: имя временного zip-файла
    """
    if os.path.exists(model_dir) and os.path.isdir(model_dir):
        print(f"[INFO] Модель уже существует в {model_dir}")
        return

    os.makedirs(os.path.dirname(model_dir), exist_ok=True)
    print(f"[INFO] Загружаем модель Vosk из Dropbox в {zip_name}...")

    try:
        with requests.get(DROPBOX_URL, stream=True) as r:
            r.raise_for_status()
            total = int(r.headers.get('content-length', 0))
            with open(zip_name, 'wb') as f:
                downloaded = 0
                for chunk in r.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
                        downloaded += len(chunk)
                        done = int(50 * downloaded / total) if total else 0
                        sys.stdout.write(f"\r[{'=' * done}{' ' * (50-done)}] {downloaded / (1024**2):.2f}MB/{total/(1024**2):.2f}MB")
                        sys.stdout.flush()
        print("\n[INFO] Загрузка завершена.")

        print(f"[INFO] Распаковываем {zip_name} в {model_dir}...")
        with zipfile.ZipFile(zip_name, 'r') as zip_ref:
            zip_ref.extractall(os.path.dirname(model_dir))
        os.remove(zip_name)
        print(f"[INFO] Модель распакована в {model_dir}")

    except Exception as e:
        print(f"[ERROR] Не удалось скачать или распаковать модель: {e}")
        sys.exit(1)


if __name__ == '__main__':
    download_model()
