# 🚖 Urban Mobility Data Explorer

## 📘 Overview
**Urban Mobility Data Explorer** is a full-stack data visualization platform built around the **New York City Taxi Trip Dataset**.  
It provides an interactive dashboard that allows users to explore patterns in taxi trips — such as trip durations, distances, and pickup times — revealing valuable insights about urban mobility in New York City.

This project demonstrates a complete **data pipeline**, from cleaning and structuring large-scale data to serving it through a backend API and visualizing it on a web-based dashboard.

---

## 🏗️ System Architecture

       ┌────────────────────────┐
       │ NYC Taxi Trip Dataset  │
       └────────────┬───────────┘
                    │
                    ▼
           ┌───────────────────┐
           │ Data Cleaning     │
           │ (Python / Pandas) │
           └────────┬──────────┘
                    │
                    ▼
           ┌───────────────────┐
           │ MariaDB Database  │
           │  - vendors        │
           │  - trips          │
           │  - locations      │
           └────────┬──────────┘
                    │
                    ▼
       ┌────────────────────────┐
       │ Backend (Flask Server) │
       │ - API Endpoints        │
       │ - DB Connection        │
       └────────┬───────────────┘
                    │
                    ▼
       ┌────────────────────────┐
       │ Frontend (HTML/JS/CSS) │
       │ - Dashboard             │
       │ - Charts & Metrics      │
       └────────────────────────┘

---

## ⚙️ Tech Stack

| Layer | Technology | Purpose |
|-------|-------------|----------|
| **Database** | MariaDB | Stores structured trip, vendor, and location data |
| **Backend** | Python (Flask) | Connects the database and serves data to the dashboard |
| **Frontend** | HTML, CSS, JavaScript | Visualizes insights interactively |
| **Containerization** | Docker, Docker Compose | Simplifies setup and deployment |
| **Data Processing** | Pandas | Cleans and transforms raw NYC trip data |

---

## 🗃️ Database Schema

### `vendors`
| Field | Type | Description |
|--------|------|-------------|
| `vendor_id` | INT | Unique ID for vendor |
| `vendor_name` | VARCHAR(50) | Name of the vendor |

### `trips`
| Field | Type | Description |
|--------|------|-------------|
| `trip_id` | BIGINT | Unique trip identifier |
| `vendor_id` | INT | Foreign key referencing `vendors` |
| `pickup_datetime` | DATETIME | Time of pickup |
| `dropoff_datetime` | DATETIME | Time of drop-off |
| `passenger_count` | INT | Number of passengers |
| `store_and_fwd_flag` | CHAR(1) | Whether trip record was stored before sending |
| `trip_duration` | INT | Duration of trip (in seconds) |
| `trip_distance_km` | DECIMAL(10,2) | Distance traveled in kilometers |
| `speed_kmph` | DECIMAL(10,2) | Average speed of trip |
| `pickup_hour` | TINYINT | Hour of pickup (0–23) |
| `pickup_dayofweek` | TINYINT | Day of week (1–7) |

### `locations`
| Field | Type | Description |
|--------|------|-------------|
| `location_id` | BIGINT | Auto-incremented primary key |
| `trip_id` | BIGINT | Foreign key referencing `trips` |
| `pickup_longitude` | DECIMAL(10,6) | Pickup longitude |
| `pickup_latitude` | DECIMAL(10,6) | Pickup latitude |
| `dropoff_longitude` | DECIMAL(10,6) | Dropoff longitude |
| `dropoff_latitude` | DECIMAL(10,6) | Dropoff latitude |

---

## 🧩 Folder Structure
NYC-Taxi-Mobility-Insights/
│
├── backend/
│ ├── algorithms/ # Analytical scripts
│ ├── db/ # Database logic
│ ├── db.py # DB connection module
│ └── server.py # Flask API server
│
├── data/
│ ├── raw/ # Original dataset
│ ├── processed/ # Cleaned dataset
│ ├── data_cleaning.py # Cleaning and transformation script
│ └── excluded_records.log # Log of excluded/invalid records
│
├── database/
│ ├── setup_db.py # Creates database & tables
│ └── insert_cleaned_taxi_data.py # Inserts processed data
│
├── frontend/
│ ├── index.html # Dashboard UI
│ ├── script.js # Data fetching & visualization logic
│ └── styles.css # UI styling
│
├── docs/
│ ├── algorithm_pseudocode.md
│ ├── architecture_diagram.png
│ └── report.pdf
│
├── logs/
│ └── excluded_records.log
│
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── README.md


---

## 🧮 Data Pipeline

1. **Raw Data Import:** Load raw NYC taxi dataset into `/data/raw`.
2. **Cleaning:** Run `data_cleaning.py` to:
   - Remove duplicates and missing values  
   - Convert timestamps and coordinates  
   - Derive new features (e.g., trip_duration, pickup_dayofweek)
3. **Database Setup:**  
   Run `setup_db.py` to create the database and tables.
4. **Data Insertion:**  
   Run `insert_cleaned_taxi_data.py` to populate tables.
5. **Backend:**  
   Flask (`server.py`) serves processed data to the frontend dashboard.
6. **Frontend Visualization:**  
   The dashboard (`index.html`, `script.js`) fetches data from the API and visualizes it with charts.

---

## 🧠 Insights and Analysis

| Insight | Description | Method |
|----------|--------------|---------|
| **Peak Pickup Hours** | Most pickups occur between 6–9 PM, indicating strong evening demand. | SQL aggregation by `pickup_hour` |
| **Distance vs Speed** | Longer trips tend to have higher average speeds due to highway travel. | Correlation query + scatter plot |
| **Vendor Performance** | Vendor #2 shows higher trip counts, suggesting better operational coverage. | Group by `vendor_id` |

---

## 💡 Design Decisions

- **Normalized relational schema** for efficient joins and aggregations  
- **TinyINT for time attributes** (hour, day) to reduce storage  
- **Indexes** on key fields (`pickup_datetime`, `pickup_dayofweek`, coordinates) for query speed  
- **Separation of concerns** between data cleaning, database logic, and backend API  
- **Dockerized setup** to ensure consistent development environments

---

## 🧱 Setup Instructions

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/Nzabinesha/NYC-Taxi-Mobility-Insights.git
cd NYC-Taxi-Mobility-Insights

### 2️⃣ Create and Activate Virtual Environment
```bash
python3 -m venv venv
source venv/bin/activate   # (Linux/Mac)
venv\Scripts\activate      # (Windows)

### 3️⃣ Install Dependencies
```bash
pip install -r requirements.txt

### 4️⃣ Set Up the Database
```bash
python database/setup_db.py
python database/insert_cleaned_taxi_data.py

### 5️⃣ Run the Backend
```bash
python backend/server.py

### 6️⃣ Open the Dashboard
```bash
http://localhost:5000
