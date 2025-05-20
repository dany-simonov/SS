import traceback
from social_network.app import create_app


app = create_app()
app.app_context().push()

print(app.url_map)
print(traceback.format_exc())

if __name__ == '__main__':
    app.run(debug=True)