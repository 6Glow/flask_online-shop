from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

import stripe

public_key = "pk_test_6pRNASCoBOKtIshFeQd4XMUh"
stripe.api_key = "sk_test_BQokikJOvBiI2HlWgH4olfQ2"


app = Flask(__name__,static_url_path="",static_folder="templates")
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///web_shop.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

YOUR_DOMAIN = "http://localhost:5000"


class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    isActive = db.Column(db.Boolean, default=True)
    date = db.Column(db.DateTime, default=datetime.utcnow())
    

    def __repr__(self):
        return self.title


@app.route('/')
def index():
    items = Item.query.order_by(Item.price).all()
    return render_template('index.html', data=items, public_key=public_key)




@app.route('/about')
def about():
    return render_template('about.html')



@app.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        title = request.form['title']
        price = request.form['price']


        items = Item(title=title, price=price)

        try:
            db.session.add(items)
            db.session.commit()
            return redirect('/')
        except:
            return "There was an error"
            

    else:
        return render_template('create.html')
    
@app.route('/thankyou')
def thankyou():
    return render_template('thankyou.html')

@app.route('/payment', methods=['POST'])
def payment():

    # CUSTOMER INFO
    customer = stripe.Customer.create(email=request.form['stripeEmail'],
                                      source=request.form['stripeToken'])

    # PAYMENT INFO
    charge = stripe.Charge.create(
        customer=customer.id,
        amount=200, # 12.00
        currency='usd',
        description='Donation'
    )

    return redirect(url_for('thankyou'))

if __name__ == '__main__':
    app.run(debug=True)
