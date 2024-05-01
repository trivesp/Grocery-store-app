from main import app
from application.security import datastore
from application.models import db, Role
from werkzeug.security import generate_password_hash


with app.app_context():
    db.create_all()

    datastore.find_or_create_role(name="admin", description="Administrator")
    datastore.find_or_create_role(name="manager", description="Store Manager")
    datastore.find_or_create_role(name="shopper", description="Common Shopper")
    db.session.commit()


    if not datastore.find_user(email="admin@email.com"):
        datastore.create_user(email="admin@email.com", password=generate_password_hash("administrator"), roles=["admin"])

    if not datastore.find_user(email="inst1@email.com"):
        datastore.create_user(email="manager1@email.com", password=generate_password_hash("manager1"), roles=["manager"], active=False)

    if not datastore.find_user(email="shop1@email.com"):
        datastore.create_user(email="shop1@email.com", password=generate_password_hash("shopper1"), roles=["shopper"])

    if not datastore.find_user(email="shop2@email.com"):
        datastore.create_user(email="shop2@email.com", password=generate_password_hash("shopper2"), roles=["shopper"])

    db.session.commit()

    # admin        =  Role(id = 0, name = 'Admin', description = 'Administrator')
    # db.session.add(admin)
    # storemanager =  Role(id = 1, name = 'Store Manager', description = 'Store Manager')
    # db.session.add(storemanager)
    # user         =  Role(id = 2,  name = 'User', description = 'Common User')
    # db.session.add(user)


    # db.session.commit()



