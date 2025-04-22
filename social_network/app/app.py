from social_network.app import create_app
from social_network.app.instance.config import BASE_DIR

app = create_app()

print(app.url_map)
print("Database URI:", app.config['SQLALCHEMY_DATABASE_URI'])
print("BASE_DIR:", BASE_DIR)


if __name__ == '__main__':
    app.run(debug=True)