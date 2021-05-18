from crm.celery import app
from reports.contrib import GenerateReport


@app.task(bind=True)
def generate_users_report(_, report_title, **kwargs):
    if report_title == 'passing_speed_report':
        GenerateReport(report_title, update_mapping=True, **kwargs).process()
    else:
        GenerateReport(report_title, **kwargs).process()
