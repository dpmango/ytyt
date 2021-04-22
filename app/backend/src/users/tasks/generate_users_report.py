from crm.celery import app


@app.task(bind=True)
def generate(_, *args, **kwargs) -> None:
    pass









