from celery import shared_task
import time


@shared_task
def test_task():

    print("===== INICIO TAREA CELERY =====")

    time.sleep(5)

    print("===== CELERY FUNCIONANDO CORRECTAMENTE =====")

    return "OK"