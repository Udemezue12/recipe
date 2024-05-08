from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from recipe_app.models import User, Recipe, Category
from recipe_app.database import db

admin = Admin(name='Recipe Admin', template_mode='bootstrap3')

admin.add_view(ModelView(User, db.session))
admin.add_view(ModelView(Recipe, db.session))
admin.add_view(ModelView(Category, db.session))
# admin.add_view(ModelView(Tag, db.session))
