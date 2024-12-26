import os

class Config:
    # Секретный ключ для сессий и csrf
    SECRET_KEY = os.environ.get('SECRET_KEY') or '3d6f45a5fc12445dbac2f59c3b6c7cb1'
    
    # Конфигурация базы данных
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///social_network.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Конфигурация загрузки файлов
    UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'app/static/uploads')
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB макс размер файла
    
    # Поддерживаемые расширения файлов для аватаров
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
