# ♻️ AI-Based Government Paper Waste Management System (Smart Audit)

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://gov-waste-management-system.streamlit.app/)
![Python](https://img.shields.io/badge/Python-3.9%2B-blue)
![License](https://img.shields.io/badge/License-MIT-green)

## 🚀 Live Demo
**Click here to view the deployed application:**
👉 **[https://gov-waste-management-system.streamlit.app/](https://gov-waste-management-system.streamlit.app/)**

---

## 📖 Project Overview

The **AI-Based Government Paper Waste Management System** is a data-driven dashboard designed to modernize how government offices track and reduce paper consumption. Unlike traditional manual audits, this system leverages **Artificial Intelligence (Linear Regression)** to predict future waste generation and creates a centralized digital ledger for accountability.

This project helps authorities move from *reactive* monitoring to *proactive* sustainability planning, classifying departments as **Gold Standard**, **Standard**, or **Non-Compliant**.

---

## ⚠️ Problem Statement

Government offices generate massive volumes of paper waste through files, reports, and administrative processes. Currently:
* **Manual Audits:** Tracking is slow, fragmented, and prone to human error.
* **No Prediction:** Authorities cannot foresee high-wastage months before they happen.
* **Lack of Accountability:** It is difficult to pinpoint which specific department is exceeding limits.
* **Data Silos:** Data is trapped in local files rather than a centralized cloud database.

---

## 🎯 Objectives

* **Digitize:** Replace manual logbooks with a cloud-based Streamlit dashboard.
* **Predict:** Use Machine Learning to forecast paper usage for the upcoming year (2026).
* **Classify:** Automatically categorize offices (Green/Yellow/Red) based on recycling rates.
* **Report:** Auto-generate official PDF Audit Reports for compliance meetings.
* **Visualize:** Provide interactive charts for "Predicted vs. Actual" usage analysis.

---

## 🛠️ Technologies Used

| Category | Tech Stack |
| :--- | :--- |
| **Frontend** | Streamlit (Python) |
| **Backend Logic** | Python, Pandas, NumPy |
| **AI / ML Model** | Scikit-Learn (Linear Regression) |
| **Database** | Supabase (PostgreSQL) |
| **Visualization** | Altair, Plotly |
| **Reporting** | FPDF (PDF Generation) |
| **Version Control** | Git & GitHub |

---

## 📂 Project Structure

```bash
gov-waste-management-system/
│
├── .streamlit/
│   └── secrets.toml       # API Keys (Not on GitHub - See Setup Guide)
│
├── services/              # Modular Logic
│   ├── db_manager.py      # Supabase Connection & CRUD
│   ├── ml_engine.py       # AI Prediction Logic
│   ├── visualizations.py  # Charts & Graphs
│   └── report_gen.py      # PDF Report Generator
│
├── main.py                # Main Streamlit Application
├── requirements.txt       # Project Dependencies
├── .gitignore             # Files to ignore (secrets, venv)
└── README.md              # Documentation
```

⚙️ Installation & Local Setup
If you want to run this project locally on your machine, follow these steps:

1. Clone the Repository
```Bash
git clone [https://github.com/Bhomaramsuthar/gov-waste-management-system.git](https://github.com/Bhomaramsuthar/gov-waste-management-system.git)
cd gov-waste-management-system
```
2. Install Dependencies
Make sure you have Python installed. Then run:

```Bash
pip install -r requirements.txt
```
3. Setup Secrets (Crucial Step!)
This project uses Supabase for the database. The API keys are hidden for security.
1. Create a folder named .streamlit in the root directory.
2. Inside it, create a file named secrets.toml.
3. Add your database credentials in the following format:
```
Ini, TOML
[supabase]
url = "YOUR_SUPABASE_URL_HERE"
key = "YOUR_SUPABASE_ANON_KEY_HERE"
```
4. Run the App
```Bash
streamlit run main.py
```
📊 Key Features / Wow Factors

1.🔮 AI Predictive Analytics:
- Trains on 2025 historical data to forecast 2026 waste generation.
- Flags "High Alert" months before they occur.

2.📝 Automated Compliance Logic:
- Uses a Decision Tree approach to classify departments.
- Handles exemptions (e.g., Confidential Records) intelligently.

3.📄 One-Click Audit Reports:
- Instantly downloads a detailed PDF report with summary statistics and AI recommendations.

4.☁️ Centralized Cloud Database:
- Real-time data syncing across all departments using Supabase.

---

## 👥 Contributors
Team EcoAudit (NBN Sinhgad Technical Institute Campus)

- Bhomaram Suthar - Full Stack Dev & AI Integration
- Hemangi Borase - Team Lead & Research
- Shreya Nawale - Data Analysis
- Adarsh Singh - Documentation
- Vanshika Birajdar - Testing
- Guided By: Prof. Sarthak Narnor

📄 License
This project is developed for the Edunet Foundation Internship.
