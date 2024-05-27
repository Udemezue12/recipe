import os
from dotenv import load_dotenv
import stripe

from flask import render_template, Blueprint, request, url_for, redirect
from recipe_app.models import Recipe, Category
from recipe_app.run import app


load_dotenv()

core = Blueprint('core', __name__)

stripe.api_key = os.getenv('STRIPE_SECRET_KEY')
public_key = os.getenv('STRIPE_PUBLIC_KEY')


# @core.route('/')
# def index():
    # page = request.args.get('page', 1, type=int)
    # recipe = Recipe.query.order_by(
    #     Recipe.rating.desc()
    # ).paginate(page=page, per_page=6)
    # return render_template('index.html')

@core.route('/')
def index():
    page = request.args.get('page', 1, type=int)
    recipe = Recipe.query.order_by(
        Recipe.title.desc()).paginate(page=page, per_page=6)
    return render_template('index.html', recipe=recipe)


@core.route('/info')
def info():
    return render_template('info.html')

@core.route('/payment', methods=['POST'])
def payment():

    # CUSTOMER INFORMATION
    customer = stripe.Customer.create(email=request.form['stripeEmail'],
                                      source=request.form['stripeToken'])

    # CHARGE/PAYMENT INFORMATION
    charge = stripe.Charge.create(
        customer=customer.id,
        amount=1999,
        currency='usd',
        description='Donation'
    )

    return redirect(url_for('core.thankyou'))