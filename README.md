**About Project**
A production-grade log generator that simulates real payment gateway distributed systems behavior using Python.
This project generates Spring Boot–style plain text logs with:
✅ Consistent traceId across services
✅ Different spanId per component
✅ Transaction-level correlation (paymentId, accountId, etc.)
✅ Cascading flows across components
✅ Log rotation (size-based)
✅ Dockerized execution
✅ CSV-driven log messages
✅ Infinite traffic simulation
Designed for observability demos, ELK/Loki testing, SRE practice.


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
6. Infinite traffic generation


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
