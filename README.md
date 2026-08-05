9
🛡️ AI Financial Auditor – Bank Transaction Fraud Detection System

📌 Overview

AI Financial Auditor is a fraud detection system that analyzes banking transactions and identifies potentially fraudulent activities using rule-based risk analysis. The application provides an interactive dashboard that allows users to monitor transaction risk levels, visualize suspicious patterns, and export audit reports.

The project simulates a real-world financial auditing environment by generating synthetic banking transaction data and evaluating each transaction based on predefined fraud detection rules.

---

✨ Features

- 🔍 Detects suspicious banking transactions.
- 📊 Interactive dashboard built with Streamlit.
- 📈 Visual analytics using Plotly.
- ⚠️ Risk scoring system (0–100).
- 🚨 Risk classification:
  - STABLE
  - ELEVATED
  - CRITICAL
- 🌍 Filter transactions by location.
- 🔎 Search transactions by sender, receiver, transaction type, or location.
- 📥 Export audit reports as CSV.
- 🔄 Generate new synthetic transaction datasets instantly.

---

🧠 Fraud Detection Logic

The system evaluates every transaction using multiple fraud indicators:

- High Volume Transfer
  
  - Large transfers above the predefined threshold receive additional risk points.

- High-Risk Locations
  
  - Transactions originating from selected high-risk regions receive a higher risk score.

- Structuring Detection
  
  - Detects transactions intentionally kept just below reporting thresholds.

- Velocity Fraud Detection
  
  - Flags accounts performing multiple transactions within a short period of time.

Each transaction receives a Risk Score between 0 and 100, then is classified into one of three risk levels.

---

🛠️ Technologies Used

- Python
- Streamlit
- Pandas
- NumPy
- Plotly Express

---

📂 Project Structure

├── app.py
├── fraud_logic.py
├── data_manager.py
├── requirements.txt
└── README.md

---

🚀 Running the Project

1. Clone the repository.

git clone <repository-link>

2. Install the required packages.

pip install -r requirements.txt

3. Run the application.

streamlit run app.py

---

📊 Dashboard

The dashboard provides:

- Financial KPIs
- Risk Distribution Scatter Plot
- Risk Level Pie Chart
- Detailed Audit Logs
- Real-Time Batch Analysis Simulation
- CSV Report Export

---

🌱 About This Project

This project is especially meaningful to me because it is my first completely independent project.

I designed, implemented, and built every part of this system from A to Z during my first year as an Artificial Intelligence student. Throughout this project, I challenged myself to learn new technologies, improve my programming skills, and understand how fraud detection systems work in the financial sector.

While there are many ways this project can be expanded and improved, it represents an important milestone in my learning journey and reflects my passion for AI, data analysis, and software development.

---

🚀 Future Improvements

- Integrate machine learning models for fraud prediction.
- Connect the application to a real database.
- Implement real-time transaction monitoring.
- Add user authentication and role management.
- Deploy the application to the cloud.
- Improve anomaly detection using advanced AI techniques.

---

👩‍💻 Author

Malak Abdelaziz

First-Year Artificial Intelligence Student
