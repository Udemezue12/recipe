

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from recipe_app.database_config import app


db = SQLAlchemy(app)
migrate = Migrate(app, db)







 

