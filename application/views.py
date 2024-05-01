from flask import current_app as app, render_template, jsonify, request, send_file
from flask_security import auth_required, roles_required
from werkzeug.security import check_password_hash, generate_password_hash
from .models import *
from .security import datastore
from flask_restful import fields, marshal
from celery.result import AsyncResult
from .mailservice import *
from .tasks import *
import flask_excel as excel
from io import BytesIO
 

# ## Endpoint for testing
# @app.get('/')
# def home():
#     # return "test screen"
#     return render_template("index.html")

# ## Endpoint for Admin Testing
# @app.get('/admin')
# @auth_required("token")
# @roles_required("admin")
# def admin():
#     return "Hello Admin"


## Endpoint for Admin activating a manager
@app.get('/activate/manager/<int:man_id>')
@auth_required("token")
@roles_required("admin")
def activate_manager(man_id):
    manager = User.query.get(man_id)
    if not manager or "manager" not in manager.roles:
        return jsonify({"message": "Manager not found"}), 404

    manager.active = True
    db.session.commit()
    return jsonify({"message": "User Activated"})


## To activate a category created by a store owner (admin user)
@app.get('/activate/category/<cat_name>')
@auth_required("token")
@roles_required("admin")
def activate_category(cat_name):
    category = db.session.query(Categories).filter(Categories.categoryname == cat_name).first()
    # category = Categories.query.get(cat_name)

    if not category:
        return jsonify({"message": "Category not found"}), 404
  
    category.categoryactive = True
    db.session.commit()
    return jsonify({"message": "Category Activated"})    

## To activate an item created by a shopper 
@app.get('/activate/item/<int:prod_id>')
@auth_required("token")
@roles_required("shopper")
def activate_item(prod_id):
    cartItem = db.session.query(cartDetails).filter(cartDetails.productId == prod_id).first()

    if not cartItem:
        return jsonify({"message": "Item not found"}), 404
  
    cartItem.cartactive = True
    db.session.commit()
    return jsonify({"message": "Item Confirmed and added to Cart."})    


# To promote a User into a Manager
@app.get('/shift/user/<int:man_id>')
@auth_required("token")
@roles_required("admin")
def shift_manager(man_id):
    shopper = User.query.get(man_id)

    if not shopper or "shopper" not in shopper.roles:
        return jsonify({"message": "User not a shopper and cannot be changed into a Manager."}), 404

    # Remove the "shopper" role
    datastore.remove_role_from_user(shopper, "shopper")
    # Add the "manager" role
    datastore.add_role_to_user(shopper, "manager")

    db.session.commit()
    return jsonify({"message": "User changed into a Manager."})


## Endpoint for login screen sign in
@app.post('/user-login')
def user_login():
    data = request.get_json()
    email = data.get('email')

    # Check if email is valid
    if not email:
        return jsonify({"message": "email not provided"}), 400

    # Fetch the email from the DB
    user = datastore.find_user(email=email)

    # Check if user exists
    if not user:
        return jsonify({"message": "User Not Found"}), 404

    #Check if passowrd is correct
    if check_password_hash(user.password, data.get("password")):
        return jsonify({"token": user.get_auth_token(), "email": user.email, "role": user.roles[0].name})
    else:
        return jsonify({"message": "Wrong Password"}), 400


# To fetch all the users
@app.get('/users')
@auth_required("token")
@roles_required("admin")
def fetch_users():
    users = User.query.all()

    if len(users) == 0:
        output =  jsonify({"message": "No Users present. Kindly add an User."})
        return output, 404

    user_list = []
    for user in users:
        user_details = {
            "id": user.id,
            "email": user.email,
            "role": user.roles[0].description if user.roles else 'No Role',
            "active": user.active
        }
        user_list.append(user_details)

    return jsonify(user_list)

# For Sign up
@app.post('/user-signup')
def user_signup():

    data = request.get_json()

    email = data.get('email')
    user = data.get('Name')
    password = data.get('password')
    password2 = data.get('password2')

    usercheck = datastore.find_user(email=email)

    if usercheck:
        return jsonify({"message": "The following mail id exists. Kindly enter a new E-mail Id."}), 400

    # Check if email is valid
    if not email:
        return jsonify({"message": "E-mail not provided"}), 400
    
    if password2 != password:
        return jsonify({"message": "The password entered is not identical to that entered in re-enter password."}), 400


    new_user = datastore.create_user(
        username=user,
        email=email,
        password=generate_password_hash(password),
        active = False
    )

    datastore.add_role_to_user(new_user, "shopper")

    
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "User created successfully."}), 200
        

########################################################

@app.route('/api/admin/categories/csv', methods=['GET'])
def download_csv2():
    # Fetch categories from the database or any other source
    categories = [
        {'name': 'Category 1', 'description': 'Description 1'},
        {'name': 'Category 2', 'description': 'Description 2'},
        # Add more categories as needed
    ]

    # Create a BytesIO object to store the CSV file
    output = BytesIO()

    # Use Flask-Excel to generate the CSV file
    excel.export_csv(output, categories, colnames=['name', 'description'], include_colnames=True)

    # Set the BytesIO object's cursor position to the beginning
    output.seek(0)

    # Define the filename for the downloaded CSV file
    filename = "categories.csv"

    # Send the file as an attachment for download
    return send_file(output, as_attachment=True, download_name=filename, mimetype='text/csv')



@app.get('/download-csv')
def download_csv():
    task = create_resource_csv.delay()
    return jsonify({"task-id": task.id})


@app.post('/get-csv/<task_id>')
def get_csv(task_id):
    res = AsyncResult(task_id)
    if res.ready():
        filename = res.result
        return send_file(filename, as_attachment=True)
    else:
        return jsonify({"message": "Task Pending"}), 404
    

@app.get('/say-hello')
def sayhello():
    t = hello.delay()
    return jsonify({"task-id":t.id})



    # cat_res = Categories.query.with_entities(
    #     Categories.categoryname

# @app.get('/download-csv')
# def download_csv():
#     cat_res = Categories.query.with_entities(
#         Categories.categoryname, Categories.categoryDescription).all()
#     csv_output =excel.make_response_from_query_sets(cat_res, ["Category Name", "Category Description"], "csv", filename = "test1.csv")
#     return csv_output
#     # task = create_resource_csv.delay()
#     # return jsonify({"task-id": task.id})


# @app.post('/get-csv/<task_id>')
# def get_csv(task_id):
#     res = AsyncResult(task_id)
#     if res.ready():
#         filename = res.result
#         return send_file(filename, as_attachment=True)
#     else:
#         return jsonify({"message": "Task Pending"}), 404