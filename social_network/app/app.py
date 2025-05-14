import traceback
from social_network.app import create_app
from social_network.app.instance.config import BASE_DIR
from social_network.app.routes import quizzes_bp

app = create_app()
app.app_context().push()
app.register_blueprint(quizzes_bp, url_prefix="/quizzes")

print(app.url_map)
print(traceback.format_exc())
# print("Database URI:", app.config['SQLALCHEMY_DATABASE_URI'])
# print("BASE_DIR:", BASE_DIR)

if __name__ == '__main__':
    app.run(debug=True)