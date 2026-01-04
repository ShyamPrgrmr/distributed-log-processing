import uuid
import threading

TRACE_REGISTRY = {}
TRACE_LOCK = threading.Lock()

def create_trace():
    trace_id = uuid.uuid4().hex
    return trace_id

def get_or_create_trace(payment_id):
    with TRACE_LOCK:
        if payment_id not in TRACE_REGISTRY:
            TRACE_REGISTRY[payment_id] = create_trace()
        return TRACE_REGISTRY[payment_id]

def new_span():
    return uuid.uuid4().hex[:16]