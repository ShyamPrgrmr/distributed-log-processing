**About Project**

A production-grade log generator that simulates real payment gateway distributed systems behavior using Python.
This project generates Spring Boot–style plain text logs with:

1. Consistent traceId across services
2. Different spanId per component
3. Transaction-level correlation (paymentId, accountId, etc.)
4. Cascading flows across components
5. Log rotation (size-based)
6. CSV-driven log messages
7. Infinite traffic simulation


**Features**
1. Spring Boot–style logs (plain text, not JSON)
2. OpenTelemetry-like tracing
	a. One traceId per transaction
	b. One spanId per service
3. Multi-component simulation
	a. API Gateway
	b. Payment Processor
	c. Risk Engine
	d. Settlement Service etc.
4. CSV-based log templates
5. Log rotation
	a. Rotate when file > 1 MB
   	b. Keep last N files
6. Infinite traffic generation (Infinite log generation cycles with multiple threads running parallely to control speed of log generation.)
7. Log creation controls using environment variables.
   ```
   a. NO_OF_TRANSACTIONS_PER_CYCLE=5000 -Transactions to create in cycle.
   b. NO_OF_THREADS_PER_CYCLE=3 -Number of threads running per cycle.
   c. MAX_LOG_SIZE=1 -Max possible size of log file in MB
   d. BACKUP_COUNT=2 -How many backup of log file to store.
   ```
8. Example logs
   ```
   2025-12-30 19:05:12.f ERROR  20062 --- [api_gateway-thread-1-0] api_gateway [traceId=1e7f988887ca4d39a56720ff48d32439 spanId=dec61aa3724a4c28 paymentId=pay_f1889166] : Request validation failed
   ```


**How It Works:**
1. Transactions are generated centrally
	a. paymentId
	b. traceId
2. Each transaction fans out to all components
3. Each component:
4. Picks a log line from its CSV
5. Generates a new spanId
6. Writes to its own log file
7. Logs rotate automatically at 1 MB
8. The cycle repeats infinitely

**How to use**

1. In Python VEnv.
   ```
   a. Create python virtual environment and activate it. 
   b. Install the dependancies using pip.
   c. Set environment variable in activate file in VEnv. 
   d. Run the main.py.
   ```
2. Using docker
	```
	a. Create docker image using docker build:
 		docker build -t <image-name> .
	b. Run the container using docker run. You can apply the environment variables as listed above.
 	```


**Project Structure**
```bash
.
├── csv
│   ├── api_gateway.csv
│   ├── authentication_service.csv
│   ├── fraud_detection.csv
│   ├── ledger_service.csv
│   ├── notification_service.csv
│   ├── payment_processor.csv
│   ├── reporting_service.csv
│   ├── risk_engine.csv
│   └── settlement.csv
├── logs
│   ├── ...
├── appLogger.py
├── csvHelper.py
├── Dockerfile
├── filters.py
├── logger.py
├── main.py
├── requirements.txt
├── setup.py
├── tracing.py
└── transactionQueue.py
```
