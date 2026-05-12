```markdown
# Telecom Intelligence 
### **Enterprise Network Predictive Analytics & Big Data Platform**

**Authors:** Arya Putatunda, Bhavmeet Singh Ahuja, Karan Sood

## Project Overview
Telecom Intelligence OS is a production-grade data engineering and machine learning platform. It transforms massive, disorganized telecommunications logs into actionable network intelligence. By processing over **15 million records**, the system identifies usage trends and employs a **Random Forest Machine Learning model** to predict regional congestion risks in real-time.

---

## Team & Task Distribution

* **Arya Putatunda**
  * **Big Data ETL:** Engineered the **PySpark** pipeline to process 15M+ records, implementing Broadcast Joins and Parquet optimization for high-speed I/O natively in a Linux environment.
  * **System Integration:** Developed the **FastAPI** orchestration layer and built the **React 18** dashboard with interactive Recharts visualizations.
  * **DevOps:** Configured the cross-platform environment (Windows + WSL Ubuntu) to host the production-grade Apache Airflow environment.
* **Bhavmeet Singh Ahuja**
  * **Intelligence Layer:** Developed the **Random Forest Classifier** and performed feature engineering (Usage Variability, Growth Rates) to achieve 90%+ prediction accuracy.
  * **Model Validation:** Managed the train-test split, verified performance via Confusion Matrices, and serialized the model for production API consumption.
* **Karan Sood**
  * **Storage Engine:** Designed the **Star Schema** Data Warehouse (Fact Usage vs. Dimension Region/Time) to support sub-second analytical queries.
  * **Workflow Orchestration:** Designed the logic for **Apache Airflow DAGs** to ensure a sequential, error-proof data lifecycle from landing zone to warehouse.

---

## System Architecture & Tech Stack

Our platform utilizes a modern data stack designed for horizontal scalability, mirroring real-world cloud infrastructure:

1. **Execution Environment:** Hybrid architecture utilizing **Windows** (UI/Backend) and **WSL/Ubuntu Linux** (Big Data/Orchestration).
2. **Ingestion Layer (`PySpark`):** Distributed processing of 15M+ raw CSV records into optimized, partitioned Parquet files.
3. **Storage Layer (`SQLite Star Schema`):** Cleaned data is structured into a Data Warehouse, separating high-volume metrics from regional metadata.
4. **Orchestration Layer (`Apache Airflow`):** Manages the automated workflow, handling file detection, schema validation, and Spark job triggering.
5. **Intelligence Layer (`Scikit-Learn`):** A Random Forest model performs proactive risk scoring on live network telemetry.
6. **Serving Layer (`FastAPI` & `React 18`):** A RESTful API provides endpoints for the frontend dashboard to visualize network health.

---

## Setup & Execution Guide

To replicate the production environment, services are split between the Linux subsystem (for heavy lifting) and the Windows host (for serving). 

### **Phase 1: The Heavy Lifting Engine (WSL Terminal)**
*Ensure you are using a WSL (Ubuntu) terminal to execute the data pipeline with native Linux Java.*

```bash
# 1. Activate the Linux environment
source ~/airflow_env/bin/activate

# 2. Build the Database (Process 15M records via PySpark)
python spark/telecom_pipeline.py

# 3. Train the AI Model (Generates serialized model.pkl)
python ml/train_model.py

```

### **Phase 2: Production Orchestration (WSL Terminals)**

*Keep WSL active to run the background workflow manager.*

```bash
# Terminal 1: Start Airflow Webserver
export AIRFLOW_HOME=~/airflow
airflow webserver --port 8080

# Terminal 2: Start Airflow Scheduler
export AIRFLOW_HOME=~/airflow
airflow scheduler

```

### **Phase 3: Application Serving (Windows Terminals)**

*Use standard Windows Command Prompt or PowerShell to serve the UI.*

```cmd
:: Terminal 3: Start FastAPI AI Backend
venv\Scripts\activate
uvicorn api.main:app --reload

:: Terminal 4: Start React Dashboard
cd react-app
npm run dev

```

---

## System Access Ports

Once all phases are executing, the platform can be accessed via the following local ports in your browser:

* 📊 **Main Dashboard (React):** `http://localhost:5173`
* ⚙️ **Pipeline Orchestrator (Airflow):** `http://localhost:8080`
* 🧠 **AI API Documentation (FastAPI):** `http://localhost:8000/docs`

---

## Repository Structure

```text
telecom-intelligence/
├── airflow/            # Airflow DAGs (WSL Production Orchestration)
├── api/                # FastAPI Application & ML Prediction Logic
├── data/               # Raw CSVs, Landing Zone, and Processed Parquet
├── ml/                 # Model Training, Feature Engineering, & .pkl files
├── react-app/          # React 18 Source Code (Modern UI Dashboard)
├── spark/              # PySpark ETL Pipeline Logic (Cross-platform compatible)
├── warehouse/          # SQL Warehouse (Star Schema implementation)
├── requirements.txt    # Project Dependencies
└── README.md           # System Documentation

```

---

## Final Verification Checklist

* [x] **PySpark Pipeline:** Verified (15,089,165 records successfully partitioned).
* [x] **Airflow DAGs:** Verified in WSL (Sequential green-status execution).
* [x] **AI Engine:** Verified (Successful batch scoring and API integration).
* [x] **React UI:** Verified (Dashboard rendering live metrics and AI predictions).

```

```