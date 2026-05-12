This is the high-caliber, production-level **README.md** for your submission. I have removed the "OS" branding, integrated the **Failure Handling (Task 3.6)** achievements, and polished the technical descriptions to meet the highest professional standards for the Prodapt assessment.

---

# 🚀 Telecom Intelligence Platform

### **Enterprise Network Predictive Analytics & Big Data Solution**

**Authors:** Arya Putatunda, Bhavmeet Singh Ahuja, Karan Sood

## 📖 Project Overview

The Telecom Intelligence Platform is a production-grade data engineering solution designed to transform massive, disorganized telecommunications logs into actionable network insights. By processing over **15 million records**, the system identifies usage patterns and employs a **Random Forest Machine Learning model** to predict regional congestion risks (Low, Medium, or High) with high precision.

---

## 👥 Team & Task Distribution

### **Arya Putatunda**

* **Data Engineering:** Architected the **PySpark ETL** pipeline for 15M+ records, implementing data partitioning and Parquet optimization.
* **Failure Handling (Task 3.6):** Developed the **Automated Data Quarantine** logic to validate ingestion integrity and isolate malformed files.
* **System Integration:** Developed the **FastAPI** backend and built the **React 18** dashboard with interactive Recharts visualizations.

### **Bhavmeet Singh Ahuja**

* **Predictive Modeling:** Developed the **Random Forest Classifier** and performed **Feature Engineering** (Usage Variability, Growth Rates) to achieve 90%+ accuracy.
* **Validation:** Managed the 80/20 train-test split and verified performance via Confusion Matrices and model serialization.

### **Karan Sood**

* **Data Warehousing:** Designed the **Star Schema** Warehouse (Fact Usage vs. Dimension Region/Time) for optimized analytical query performance.
* **Workflow Orchestration:** Designed the **Apache Airflow DAG** logic (WSL-based) to ensure an idempotent and sequential data lifecycle.

---

## 🏗 System Architecture

The platform utilizes a robust data stack designed for horizontal scalability.

1. **Ingestion & Quarantine:** Raw data enters the `/landing` zone. Our automated validation script performs integrity checks; valid data moves to `/raw`, while malformed files are moved to `/rejected`.
2. **Big Data Processing:** PySpark processes the 15M+ record volume from the validated raw zone using distributed computing.
3. **Storage Layer:** Data is structured into a **SQL Star Schema**, separating high-volume metrics from regional/temporal metadata for sub-second reporting.
4. **Intelligence Layer:** A **Random Forest** model performs proactive risk scoring on live network telemetry via modular FastAPI endpoints.

---

## 💻 Setup & Execution

### **1. Environment Setup**

Ensure you have **Python 3.10+**, **Node.js**, and **WSL** (for Airflow) installed.

```bash
# Install required Python packages
pip install -r requirements.txt

```

### **2. Database & Model Generation**

These scripts must be executed in order to populate the local environment.

```bash
# A. Build the SQL Warehouse & Process 15M records
python spark/telecom_pipeline.py

# B. Train the AI Model (Generates ml/model.pkl)
python ml/train_model.py

```

### **3. Workflow Orchestration (WSL/Airflow)**

1. Open WSL: `source ~/airflow_env/bin/activate`
2. Start Services: `airflow webserver --port 8080` & `airflow scheduler`
3. Access **`http://localhost:8080`** and trigger the **`telecom_ingestion_pipeline`** DAG.

### **4. Launch the Application**

```bash
# Terminal A: Backend API
uvicorn api.main:app --reload

# Terminal B: Frontend UI
cd react && npm install && npm run dev

```

---

## 📁 Repository Structure

```text
telecom-intelligence/
├── airflow/dags/       # Airflow DAGs (Functional WSL Orchestration)
├── api/routes/         # Modular FastAPI endpoints (Analytics & ML)
├── data/               # Ingestion Zones: /landing, /raw, /rejected, /processed
├── docs/               # System Design Document & Architecture Diagram
├── ml/                 # Random Forest training & serialized .pkl model
├── react/              # React 18 Source Code (Dashboard UI)
├── spark/              # PySpark ETL & validate_landing.py (Task 3.6)
├── warehouse/          # SQLite Star Schema implementation
└── requirements.txt    # Project Dependencies

```

---

## 🧹 Submission Checklist

* [x] **Failure Handling verified:** Corrupt data isolated in `/rejected` directory.
* [x] **PySpark Pipeline verified:** 15M records successfully partitioned and warehouse updated.
* [x] **Airflow DAGs verified:** Sequential, green-status execution in WSL.
* [x] **API Modularity verified:** Separate routes for Analytics and AI predictions.
* [x] **UI verified:** Dashboard rendering live metrics and ML Risk predictions.

---
