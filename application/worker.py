from celery import Celery, Task
from flask import current_app as app


# class FlaskTask(Task):
#     def __call__(self, *args: object, **kwargs: object) -> object:
#         with app.app_context():  # Assuming 'app' is accessible here
#             return self.run(*args, **kwargs)

# def celery_init_app(app):
#     celery_app = Celery(app.name, task_cls=FlaskTask)  # Use the defined class
#     celery_app.config_from_object("celeryconfig")
#     return celery_app

# def celery_init_app(app):
#     class FlashTask(Task):
#         def __call__(self, *args: object, **kwargs: object) -> object:
#             with app.app_context():  # Assuming 'app' is accessible here
#                 return self.run(*args, **kwargs)
            
#     celery_app = Celery(app.name, task_cls=FlashTask)  # Use the defined class
#     celery_app.config_from_object("celeryconfig")
#     return celery_app


class FlashTask(Task):
    def __call__(self, *args: object, **kwargs: object) -> object:
        with app.app_context():  # Assuming 'app' is accessible here
            return self.run(*args, **kwargs)

def celery_init_app(app):
    celery_app = Celery(app.name, task_cls=FlashTask)
    celery_app.config_from_object("celeryconfig")
    return celery_app
