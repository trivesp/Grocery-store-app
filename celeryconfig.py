broker_url = "redis://localhost:6379/1"
result_backend = "redis://localhost:6379/2"
timezone = "Asia/kolkata"
broker_connection_retry_on_startup=True
include = ['workertest']

##COmmand 
# Celery (in CMD under correct path): C:\Users\S.TRIVEDHAN\AppData\Local\Packages\PythonSoftwareFoundation.Python.3.9_qbz5n2kfra8p0\LocalCache\local-packages\Python39\Scripts\celery.exe -A application.worker worker --loglevel INFO
# Redis (Under Linux Shell): sudo service redis-server start   
### redis-cli