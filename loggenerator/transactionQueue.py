import uuid
from appLogger import normal_app_logger
normLogger = normal_app_logger()

class Transaction:
    def __init__(self, payment_id, trace_id):
        self.payment_id = payment_id
        self.trace_id = trace_id

def generate_transactions(n):
    txns = []
    normLogger.info(f"Generating {n} transactions.")
    for _ in range(n):
        payment_id = f"pay_{uuid.uuid4().hex[:8]}"
        trace_id = uuid.uuid4().hex
        txns.append(Transaction(payment_id, trace_id))
    return txns
