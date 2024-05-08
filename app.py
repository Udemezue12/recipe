from flask import render_template
from recipe_app.run import app



# @app.errorhandler(404)
# def page_not_found(e):
#     return render_template("error_pages/404.html"), 404

if __name__ == '__main__':
    app.run(port=2000)
