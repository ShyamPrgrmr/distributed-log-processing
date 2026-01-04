import pandas as pd
import threading
import os
import time
from logger import service_worker
from transactionQueue import generate_transactions
from appLogger import normal_app_logger
from setup import getLogsPath
normLogger = normal_app_logger()
from constants import *

normLogger.info("Started")

NoOfTransactions = DEFAULT_NO_OF_TRANSACTIONS_PER_CYCLE if os.environ.get(NO_OF_TRANSACTIONS_PER_CYCLE)==None else os.environ.get(NO_OF_TRANSACTIONS_PER_CYCLE)
normLogger.info("Number of transactions per cycle : {}".format(NoOfTransactions))

ThreadsPerCycle = DEFAULT_THREADS_PER_LOG if os.environ.get(NO_OF_THREADS_PER_CYCLE)==None else os.environ.get(NO_OF_THREADS_PER_CYCLE)
normLogger.info("Threads per cycle : {}".format(ThreadsPerCycle))

os.makedirs(LOG_DIR, exist_ok=True)
normLogger.info("Log Directory : {}".format(LOG_DIR))

LogToUse = os.environ.get(LOG_TO_USE)
components = DEFAULT_COMPONENT if LogToUse == None else getLogsPath(LogToUse)
normLogger.info(f"Component selected for logging: {components}")

cycle = 1

try:
    while True:
        normLogger.info(f"Starting cycle {cycle}")
        transactions = generate_transactions(int(100 if NoOfTransactions==None else NoOfTransactions))
        threads = []
        for comp in components:
            for i in range(0,int(ThreadsPerCycle)):
                t = threading.Thread(
                    target=service_worker,
                    name=THREAD_NAME.format(comp,cycle,i),
                    args=(comp, transactions, cycle)
                )
                t.start()
                threads.append(t)
                
        for t in threads:
            t.join()
        normLogger.info("Completed logs generation cycle {}".format(str(cycle)))
        cycle += 1
        time.sleep(1)

except KeyboardInterrupt:
    normLogger.info("Shutting down log generator gracefully...")








