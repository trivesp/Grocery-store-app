from flask_sqlalchemy import SQLAlchemy
from flask_security import UserMixin, RoleMixin
from flask_security import auth_required, roles_required, roles_accepted, current_user


engine = None
db = SQLAlchemy()


## RBAC LOGIN MODELS

class RolesUsers(db.Model):
    __tablename__ = 'roles_users'
    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column('user_id', db.Integer(), db.ForeignKey('user.id'))
    role_id = db.Column('role_id', db.Integer(), db.ForeignKey('role.id'))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=False)
    email = db.Column(db.String, unique=True)
    password = db.Column(db.String(255))
    active = db.Column(db.Boolean())
    fs_uniquifier = db.Column(db.String(255), unique=True, nullable=False)
    roles = db.relationship('Role', secondary='roles_users',
                         backref=db.backref('users', lazy='dynamic'))

    
class Role(db.Model, RoleMixin):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))


###########################################################


## Other Models


class Categories(db.Model):

    __tablename__       = "Categories"
    categoryid           = db.Column(db.Integer, autoincrement=True, primary_key=True, nullable = False)
    categoryname         = db.Column(db.Text, nullable = False)
    categoryDescription  = db.Column(db.Text, nullable = False)
    categoryactive       = db.Column(db.Boolean(),  nullable = False)     
    # creator_id           = db.Column(db.Integer, db.ForeignKey('User.id'), nullable=False) 


class Products(db.Model):
    __tablename__       = "Products"
    productId           = db.Column(db.Integer, autoincrement=True, primary_key=True, nullable = False)
    categoryId          = db.Column(db.Integer,db.ForeignKey('Categories.categoryid'), nullable = False)
    productName         = db.Column(db.Text, nullable = False)
    ProductDescription  = db.Column(db.Text, nullable = False)
    price               = db.Column(db.Numeric, nullable = False)
    quantity            = db.Column(db.Numeric, nullable = False)
    uom                 = db.Column(db.Text, nullable = False)
    category = db.relationship('Categories', backref='products', lazy=True)


class cartDetails(db.Model):
    __tablename__   = "cartDetails"
    cardId          = db.Column(db.Integer, autoincrement=True, primary_key=True, nullable = False)
    userId          = db.Column(db.Integer,db.ForeignKey('user.id'),  nullable = False)
    productId       = db.Column(db.Integer, db.ForeignKey('Products.productId'),  nullable = False)
    qtyrequested    = db.Column(db.Numeric, nullable = False)
    netprice        = db.Column(db.Numeric, nullable = False)
    cartactive      = db.Column(db.Boolean(),nullable = False)    
    user            = db.relationship('User', backref=db.backref('cartDetails', lazy=True))
    product         = db.relationship('Products', backref=db.backref('cartDetails', lazy=True))   


class OrderDetails(db.Model):
    __tablename__   = "OrderDetails"
    orderId         = db.Column(db.Integer, autoincrement=True, primary_key=True, nullable = False)
    userId          = db.Column(db.Integer,db.ForeignKey('user.id'),  nullable = False)
    orderDate       = db.Column(db.DateTime, nullable = False)
    orderstatus     = db.Column(db.Text, nullable = False)
    items           = db.Column(db.JSON, nullable = False)
    totalprice      = db.Column(db.Numeric(10,2), nullable = False)
    user            = db.relationship('User', backref=db.backref('OrderDetails', lazy=True))



# class OrderDetails(db.Model):
#     __tablename__   = "OrderDetails"
#     orderId         = db.Column(db.Integer, autoincrement=True, primary_key=True, nullable = False)
#     userId          = db.Column(db.Integer,db.ForeignKey('User.id'),  nullable = False)
#     orderDate       = db.Column(db.Text)
#     totalAmount     = db.Column(db.Numeric, nullable = False)
#     # user            = db.relationship('UserDetails', backref=db.backref('OrderDetails', lazy=True))

# class OrderItemsDetails(db.Model):
#     __tablename__   = "OrderItemsDetails"
#     orderItemsId    = db.Column(db.Integer, autoincrement=True, primary_key=True, nullable = False)
#     orderId         = db.Column(db.Integer,db.ForeignKey('OrderDetails.orderId'),  nullable = False)
#     productId       = db.Column(db.Integer, db.ForeignKey('Products.productId'),  nullable = False)
#     quantity        = db.Column(db.Numeric, nullable = False)
#     price           = db.Column(db.Numeric, nullable = False)
#     order           = db.relationship('OrderDetails', backref=db.backref('OrderItemsDetails', lazy=True))
#     product         = db.relationship('Products', backref=db.backref('OrderItemsDetails', lazy=True))

# class cartDetails(db.Model):
#     __tablename__   = "cartDetails"
#     cardId          = db.Column(db.Integer, autoincrement=True, primary_key=True, nullable = False)
#     userId          = db.Column(db.Integer,db.ForeignKey('User.id'),  nullable = False)
#     productId       = db.Column(db.Integer, db.ForeignKey('Products.productId'),  nullable = False)
#     quantity        = db.Column(db.Numeric, nullable = False)
#     dateAdded       = db.Column(db.Numeric )
#     itemPrice       = db.Column(db.Numeric, nullable = False)
#     user            = db.relationship('User', backref=db.backref('cartDetails', lazy=True))
#     product         = db.relationship('Products', backref=db.backref('cartDetails', lazy=True))   



    