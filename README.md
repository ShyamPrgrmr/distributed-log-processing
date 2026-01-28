# Logs Infrastructure – Docker Compose Setup

This project sets up a **log ingestion and processing pipeline** using Docker Compose.  
It simulates application logs, ships them via Fluentd to Kafka, processes them with Logstash, and finally indexes them into Elasticsearch and Kibana.

---

## 🧱 Architecture Overview

**Flow:**

![Architecture Diagram](Flow Diagram.drawio.svg)


---

## 📦 Services Included

- **Log Generator** – Generates application logs
- **Fluentd** – Collects logs from shared volume and forwards to Kafka
- **Kafka (KRaft)** – Controller + Broker setup
- **Logstash** – Consumes logs from Kafka and pushes to Elasticsearch
- **Elasticsearch**
  - Coordination node
  - Data node
  - Init container for templates / index setup

---

## ✅ Prerequisites

Make sure you have the following installed:

- Docker `>= 24`
- Docker Compose `>= v2`
- At least **6–8 GB RAM** allocated to Docker

---

## 📁 Project Structure

```

.
├── docker-compose.yml
├── fluentd/
├── logstash/
├── loggenerator/
├── kafka/
│   ├── conf/
│   └── data/
├── elasticsearch/
│   ├── coordination_node/
│   ├── data_node/
│   └── elasticsearch-init/

````

---

## 🌐 Required Docker Network & Volumes

This setup uses **external volumes and network**, so they must be created manually **before starting**.

### Create Docker Network

```bash
docker network create logs-network
````

### Create Docker Volumes

```bash
docker volume create logs-storage
docker volume create es-data
```

---

## ▶️ How to Run the Project

### Step 1: Clone the Repository

```bash
git clone https://github.com/ShyamPrgrmr/distributed-log-processing.git
cd distributed-log-processing
```

---

### Step 2: Configure Environment Files

Ensure all `.env` files exist and are properly configured:

* `loggenerator/.env`
* `fluentd/.env`
* `kafka/conf/.controller.env`
* `kafka/conf/.broker.env`
* `logstash/.env`
* `elasticsearch/**/.env`

---

### Step 3: Start the Stack

```bash
docker compose up -d --build
```

This will:

* Build custom images
* Start Kafka (controller first, then broker)
* Bring up Fluentd, Logstash, and Elasticsearch
* Run Elasticsearch init container once

---

### Step 4: Verify Running Containers

```bash
docker compose ps
```

All services should be in **running** state except `es-init` (expected to exit after completion).

---

## 🔍 Useful Checks

### Kafka Broker

```bash
docker logs kafka-broker-1
```

### Fluentd

```bash
docker logs fluentd
```

### Logstash

```bash
docker logs logstash
```

### Elasticsearch Health

```bash
curl http://localhost:9200/_cluster/health?pretty
```

(If exposed via port mapping)

---

## 🧹 Stopping the Stack

```bash
docker compose down
```

---

## 🗑️ Full Cleanup (Optional)

If you want a **fresh start**:

```bash
docker compose down -v
docker volume rm logs-storage es-data
docker network rm logs-network
```

---

## 📌 Notes

* Kafka runs in **KRaft mode** (no Zookeeper).
* Fluentd uses a **position file** to handle log rotation safely.
* Elasticsearch data persists across restarts.
* `es-init` runs once to configure index templates.

---

## 🚀 Next Improvements (Optional)

* Add Kafka UI (AKHQ / Kafdrop)
* Add Elasticsearch index lifecycle policies
* Scale Kafka brokers

---

## 🧠 Maintained By

Shyam Pradhan
```bash
Feel free to fork, experiment, and extend 🚀
```
