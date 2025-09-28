# Spreadsheet2API

Spreadsheet2API is a modern FastAPI-based web application that allows users to upload Excel spreadsheets (`.xls` / `.xlsx`) and instantly turn them into a queryable API. It also includes a web interface for testing your uploaded tables with search, filter, and limit options.

---

## Features

- Upload Excel spreadsheets and automatically create API endpoints.
- Query your spreadsheet data directly via a web interface or REST API.
- Filter columns, search for keywords, and limit results.
- Modern, responsive interface with consistent styling.
- All uploaded tables are listed in a dropdown for easy selection.
- Works without writing any backend code.

---

## Demo

After running the app, visit:

- **Upload Page:** `http://127.0.0.1:8000/upload` – Upload your Excel files.
- **Query Tester:** `http://127.0.0.1:8000/query` – Interactively test your API endpoints.

---

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/abu-pixel/Spreadsheet2API.git
   cd Spreadsheet2API
2 Create and activate a virtual environment:
python -m venv .venv
.venv\Scripts\activate   # Windows
# OR
source .venv/bin/activate  # Mac/Linux
3 Install dependencies:
pip install -r requirements.txt
4 Run the application:
uvicorn app:app --reload --port 8000


Usage

Open your browser and go to http://127.0.0.1:8000/upload.

Upload an Excel spreadsheet.

After upload, view the automatically generated API endpoint.

Go to http://127.0.0.1:8000/query to test queries with:

Limit: Number of rows to return.

Search: Keyword search across all columns.

Filter: Filter by specific column and value.

Folder Structure
Spreadsheet2API/
│
├─ app.py               # Main FastAPI application
├─ requirements.txt     # Python dependencies
├─ static/              # CSS and JS files
├─ templates/           # HTML templates
├─ uploads/             # Uploaded Excel files
└─ .venv/               # Python virtual environment (optional)

Notes

This project does not require a database; all data is kept in memory (Pandas DataFrames) and will reset on app restart.

For persistent storage, consider saving uploaded Excel files to a database.

Recommended for quick demos, client testing, or internal tools.
