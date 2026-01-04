import pandas as pd
import logging
import time
import random

from setup import setup_logger
from tracing import new_span

from csvHelper import load_csv
from appLogger import normal_app_logger
normLogger = normal_app_logger()


def service_worker(component, transactions, cycle):
    normLogger.info("Cycle: {} : {} - thread started creating logs".format(str(cycle),component))
    logger = setup_logger(component)
    df = load_csv(component)

    for txn in transactions:
        row = df.sample(1).iloc[0]

        span_id = new_span()

        logger.log(
            level=getattr(logging, row.level),
            msg=row.log,
            extra={
                "traceId": txn.trace_id,
                "spanId": span_id,
                "paymentId": txn.payment_id
            }
        )

        time.sleep(random.uniform(0.01, 0.1))

    normLogger.info("{} - thread stopped creating logs".format(component))




