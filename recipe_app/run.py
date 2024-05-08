import os
from flask import Flask
from dotenv import load_dotenv
from flask_wtf.csrf import CSRFProtect
from whitenoise import WhiteNoise



load_dotenv()

app = Flask(__name__)
app.wsgi_app = WhiteNoise(app.wsgi_app, root='recipe_app/static')

secret_key = os.getenv('SECRET_KEY')
if secret_key is None:
    raise ValueError("SECRET_KEY not found in environment variables")

app.config['SECRET_KEY'] = secret_key


# Initialize CSRF protection
csrf = CSRFProtect(app)


# if __name__ == '__main__':
#     app.run(port=7000)


