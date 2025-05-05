from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime,date,timedelta
from faker import Faker
import random

fake = Faker()

app = Flask(__name__)
app.config.from_pyfile('config.cfg')

db = SQLAlchemy(app)

class Customer(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    first_name = db.Column(db.String(50), nullable = False)
    last_name = db.Column(db.String(50), nullable = False)
    address = db.Column(db.String(500), nullable = False)
    city = db.Column(db.String(50), nullable = False)
    postcode = db.Column(db.String(50), nullable = False)
    email = db.Column(db.String(50), nullable = False, unique = True)
    
    #the backref means that the customer.order can have many outputs (1 customer can have many orders), but the order.customer can have one output (the customer id that the order belongs)
    orders = db.relationship('Orders', backref='customer')

order_product = db.Table('order_product',
                         db.Column('order_id',db.Integer, db.ForeignKey('orders.id'), primary_key = True),
                         db.Column('product_id',db.Integer, db.ForeignKey('product.id'), primary_key = True)
                         ) 
    
class Orders(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    order_date = db.Column(db.DateTime, nullable = False, default = date.today())
    ship_date = db.Column(db.DateTime)
    delivered_date = db.Column(db.DateTime)
    cupon_code = db.Column(db.String(50))
    
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'), nullable = False)
    
    #the secondary is the association table where it needs to go through to get the product
    products = db.relationship('Product', secondary=order_product, backref='orders')
     
     
    def __repr__(self):
        return f"Orders({self.id},{self.order_date},{self.ship_date},{self.delivered_date},{self.cupon_code},{self.customer_id})"
     
class Product(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(30), nullable = False, unique = True) # nullable = False <- cannot be null
    price = db.Column(db.Integer, nullable = False)
    
    
    
    
def add_customers():
    for _ in range(100):
        customer = Customer(
            first_name=fake.first_name(),
            last_name=fake.last_name(),
            address=fake.street_address(),
            city=fake.city(),
            postcode=fake.postcode(),
            email=fake.email()
        )
        db.session.add(customer)
    db.session.commit()
    
    
def add_orders():
    customers = Customer.query.all()
    
    for _ in range(1000):
        customer = random.choice(customers)
        
        ordered_date = fake.date_this_year()
        shipped_date = random.choices([None,fake.date_time_between(start_date=ordered_date)], [10,90])[0]
        
        delivered_date = None
        if shipped_date:
            delivered_date = random.choices([None,fake.date_time_between(start_date=ordered_date)], [50,50])[0]
            
        cupon_code = random.choices([None,'50OFF','FREESHIPPING','BUYONEGETONE'], [80,5,10,5])[0]
        
        order = Orders(
            order_date=ordered_date,
            ship_date=shipped_date,
            delivered_date=delivered_date,
            cupon_code=cupon_code,
            customer_id=customer.id
        )
        db.session.add(order)
    db.session.commit()
    
def add_products():
    for _ in range(8):
        product = Product(
            name=fake.color_name(),
            price=random.randint(10,100)
        )
        db.session.add(product)
    db.session.commit()
    
def add_order_products():
    orders = Orders.query.all()
    products = Product.query.all()
    
    for order in orders:
        k = random.randint(1,3)
        
        purchased_products = random.sample(products, k)
        order.products.extend(purchased_products)
    
    db.session.commit()
    
def create_random_data():
    db.create_all()
    add_customers()
    add_orders()
    add_products()
    add_order_products()
    
def orders_by_customer_id(customer_id: int):
    print('Get Orders by Customer')
    orders = Orders.query.filter_by(customer_id == customer_id).all()
    for order in orders:
        print(order.id)
        
def get_pending_orders():
    print('Pending Orders')
    pending_orders = Orders.query.filter(Orders.ship_date.is_(None)).order_by(Orders.order_date.desc()).all()
    for pending_order in pending_orders:
        print(pending_order.order_date)
    
    
def how_many_customers():
    print('How many customers?')
    print(Customer.query.count())
    
def orders_with_code():
    print('Orders with cupon code.')
    for order in Orders.query.filter(Orders.cupon_code.isnot(None)).filter(Orders.cupon_code != 'FREESHIPPING').order_by(Orders.id).all():
        print(order.id)
            
def revenue_in_last_x_days(x_days=30):
    print(f'Revenue in past {x_days} days:')
    print(db.session
          .query(db.func.sum(Product.price))
          .join(order_product)
          .join(Orders)
          .filter(Orders.order_date > (datetime.now() - timedelta(days=x_days)))
          .scalar()
        )
    
def average_fulfillment_time():
    print('Avereage fulfillment time')
    print(db.session
            .query(
                db.func.sec_to_time(
                    db.func.avg(
                                db.func.timediff(Orders.ship_date,Orders.order_date)
                    )
                )
            )
            .filter(Orders.ship_date.isnot(None))
            .scalar()
        )
    
def get_customers_who_have_purchased_x_dollars(x=500):
    print(f'get customers who have purchased {x} dollars')
    customers = db.session.query(Customer).join(Orders).join(order_product).join(Product).group_by(Customer).having(db.func.sum(Product.price) > x).all()
    for customer in customers:
        print(customer.first_name + " " + customer.last_name)
        
        