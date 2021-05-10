from crm.celery import app
from reports.contrib import GenerateReport


@app.task(bind=True)
def generate_users_report(_, *args, **kwargs):
    GenerateReport(*args, **kwargs).process()

