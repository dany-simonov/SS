import traceback

from social_network.app import create_app
from social_network.app.instance.config import BASE_DIR

app = create_app()
app.app_context().push()

print(app.url_map)
print(traceback.format_exc())
# print("Database URI:", app.config['SQLALCHEMY_DATABASE_URI'])
# print("BASE_DIR:", BASE_DIR)

if __name__ == '__main__':
    app.run(debug=True)