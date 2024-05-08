from flask import render_template, redirect, request, Blueprint, url_for, abort, flash, abort

from flask_login import current_user, login_required
from recipe_app.models import Category, Recipe
from recipe_app.recipe.forms import RecipeForm
from recipe_app.category.forms import CategoryForm

from recipe_app.database import db
from recipe_app.users.picture_handler import save_picture


recipe = Blueprint('recipe', __name__)


@recipe.route('/create_recipe', methods=['GET', 'POST'])
# @login_required
def create_recipe():
    form = RecipeForm()
    if form.validate_on_submit():
        if current_user.is_authenticated:
            picture_file = None
            if form.picture.data:
                picture_file = save_picture(form.picture.data)
            recipe = Recipe(
                title=form.title.data,
                instructions=form.instructions.data,
                cooking_time=form.cooking_time.data,
                ingredients=form.ingredients.data,
                carbs = form.carbs.data,
                protein = form.protein.data,
                calories = form.calories.data,
                rating = form.rating.data,
                fat = form.fat.data,
                difficulty = form.difficulty.data,
                user_id=current_user.id,
                category_id=form.category.data,
               
            )
            selected_categories = Category.query.filter(
                Category.id.in_(form.categories.data)).all()
            recipe.categories.extend(selected_categories)
            db.session.add(recipe)
            db.session.commit()
            flash('You successfully created a recipe')
            return redirect(url_for('core.index'))
        else:
            flash('You must be logged in to create a recipe.', )
            return redirect(url_for('users.login'))
    return render_template('create_recipe.html', form=form)


@recipe.route('/<int:recipe_id>/update', methods=['GET', 'POST'])
@login_required
def update(recipe_id):
    recipe = Recipe.query.get_or_404(recipe_id)
    form = RecipeForm(obj=recipe)
    if recipe.author != current_user:
        abort(403)

    if request.method == 'POST' and form.validate_on_submit():

        form.populate_obj(recipe)
        db.session.commit()
        flash('Recipe successfully updated')
        return redirect(url_for('recipe.recipes', recipe_id=recipe_id))
    return render_template('view_recipe.html', recipe=recipe, form=form)


@recipe.route('/delete_recipe/<int:recipe_id>', methods=['GET', 'POST'])
@login_required
def delete_recipe(recipe_id):
    recipe = Recipe.query.get_or_404(recipe_id)
    if recipe.author != current_user:
        abort(403)
    db.session.delete(recipe)
    db.session.commit()
    flash('Recipe has been deleted')
    return redirect(url_for('core.index'))


@recipe.route('/<int:recipe_id>')
def recipes(recipe_id):
    recipe = Recipe.query.get_or_404(recipe_id)
    return render_template('recipe.html', title=recipes.title, date=recipes.date, post=recipes)


# ///////////////////////////////////////////////////////////////////////////


@recipe.route('/category/<int:category_id>', methods=['GET', 'POST'])
def category_details(category_id):
    category = Category.query.get_or_404(category_id)
    recipes = category_id.Recipe
    return render_template('category_details.html', category=category, recipes=recipes)


# @recipe.route('/<int:category_id>')
# def categories():
#     categori


@recipe.route('/category/new', methods=['GET', 'POST'])
# @login_required
def new_category():
    form = CategoryForm()
    if form.validate_on_submit():
        category = Category(
            name=form.name.data
        )

        db.session.add(category)
        db.session.commit()
        flash('Category created successfully!')
        return redirect(url_for('core.index'))
    return render_template('new_category.html', form=form)


@recipe.route('/delete_category/<int:category_id>', methods=['GET', 'POST'])
@login_required
def delete_category(category_id):
    category = Category.query.get_or_404(category_id)
    if category.author != current_user:
        flash('You are not authorized to delete this category.', 'danger')
        return redirect(url_for('core.index'))
    db.session.delete(category)
    db.session.commit()
    flash('Recipe has been deleted')
    return redirect(url_for('core.index'))
