from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, TextAreaField, IntegerField, SubmitField, SelectField, FloatField
from wtforms.validators import DataRequired, Length, NumberRange
from recipe_app.models import Category


class RecipeForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(max=100)])
    instructions = TextAreaField('Instructions', validators=[DataRequired()])
    cooking_time = IntegerField('Cooking Time (minutes)', validators=[
                                DataRequired(), NumberRange(min=1)])
    ingredients = TextAreaField('Ingredients', validators=[DataRequired()])
    picture = FileField('Update Profile Picture', validators=[
                        FileAllowed(['jpg', 'png'])])
    category = SelectField('Category', coerce=int)
    rating = FloatField('Rating', render_kw={'type': 'hidden'})
    calories = FloatField('Calories')
    protein = FloatField('Protein')
    carbs = FloatField('Carbohydrates')
    fat = FloatField('Fat')
    difficulty = StringField('Difficulty')
    

    submit = SubmitField('Create Recipe')

    def __init__(self, *args, **kwargs):
        super(RecipeForm, self).__init__(*args, **kwargs)
        self.populate_categories()
        

    def populate_categories(self):
        self.category.choices = [(category.id, category.name)
                                 for category in Category.query.all()]

  


class RecipeDeleteForm(FlaskForm):
    submit = SubmitField('Delete Recipe')
