import os
import gdown
import zipfile

def download_model():
    model_path = "models/model"
    if not os.path.exists(model_path):
        print("[INFO] Загрузка модели Vosk...")
        url = "https://drive.google.com/uc?id=1OXogMt5BpI7ZcImV2opafFzR7fTj5fPk"
        output = "models/model.zip"

        os.makedirs("models", exist_ok=True)
        gdown.download(url, output, quiet=False)

        print("[INFO] Распаковка модели...")
        with zipfile.ZipFile(output, 'r') as zip_ref:
            zip_ref.extractall("models")
        os.remove(output)

        print("[INFO] Модель успешно загружена и распакована.")
    else:
        print("[INFO] Модель уже загружена.")

if __name__ == "__main__":
    download_model()
