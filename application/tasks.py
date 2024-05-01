from celery import shared_task
from .models import Categories
import flask_excel as excel
from .mailservice import send_message
from .models import User, Role
from jinja2 import Template

from werkzeug.security import check_password_hash
from flask import  jsonify, request
from .security import datastore



@shared_task(ignore_result=False)
def hello():
    return "help"


@shared_task(ignore_result=False)
def create_resource_csv():
    cat_res = Categories.query.with_entities(
        Categories.categoryname, Categories.categoryDescription).all()

    csv_output = excel.make_response_from_query_sets(
        cat_res, ["name", "description"], "csv")
    filename = "test.csv"

    with open(filename, 'wb') as f:
        f.write(csv_output.data)

    return filename


@shared_task(ignore_result=True)
def daily_reminder(to, subject):
    users = User.query.filter(User.roles.any(Role.name == 'admin')).all()
    for user in users:
        with open('test.html', 'r') as f:
            template = Template(f.read())
            send_message(user.email, subject,
                         template.render(email=user.email))
    return "OK"