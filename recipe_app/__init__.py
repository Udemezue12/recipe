from recipe_app.core.views import core
from recipe_app.run import app
from recipe_app.error_pages.handlers import error_pages
from recipe_app.login import login_manager
from recipe_app.users.views import users
from recipe_app.recipe.views import recipe


app.register_blueprint(core)
app.register_blueprint(error_pages)
app.register_blueprint(users)
app.register_blueprint(recipe)



login_manager.init_app(app)
