# 🧪 Product Review ETL Pipeline (Python Project)

This is a beginner-friendly data engineering project built in pure Python.  
It extracts raw product reviews from a CSV file, transforms the data, and loads the cleaned version into both a Parquet file and a SQLite database.

---

## 🔧 What It Does

✔️ Extracts raw data from `product_reviews.csv`  
✔️ Cleans text (lowercase, strips punctuation)  
✔️ Validates dates  
✔️ Adds a new column: `review_length`  
✔️ Saves cleaned data to:
- A compressed Parquet file  
- A SQL table (`product_reviews` in `reviews.db`)  
✔️ Logs all steps

---

## ▶️ How to Run

1. Install dependencies:
```bash
pip install -r requirements.txt
