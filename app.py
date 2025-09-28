import os
import pandas as pd
from fastapi import FastAPI, UploadFile, File, Form
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Allow CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Upload folder
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# In-memory storage of dataframes
DATAFRAMES = {}

# Mount static folder
app.mount("/static", StaticFiles(directory="static"), name="static")

# Home route
@app.get("/", response_class=HTMLResponse)
async def root():
    html = """
    <html>
    <head>
        <title>Spreadsheet2API</title>
        <link rel="stylesheet" href="/static/style.css">
    </head>
    <body>
        <h1>Spreadsheet2API</h1>
        <p>Upload a file at <a href="/upload">Upload</a> or test queries at <a href="/query">Query Tester</a>.</p>
    </body>
    </html>
    """
    return HTMLResponse(content=html)

# Upload page
@app.get("/upload", response_class=HTMLResponse)
async def upload_page():
    html = """
    <html>
    <head>
        <title>Upload Spreadsheet</title>
        <link rel="stylesheet" href="/static/style.css">
    </head>
    <body>
        <h1>Upload Spreadsheet</h1>
        <form action="/upload" method="post" enctype="multipart/form-data">
            <input type="file" name="file" required>
            <button type="submit">Upload</button>
        </form>
        <h2>Available Tables</h2>
        <ul>
        {% for table in tables %}
            <li>{{ table }} — <a href="/api/{{ table }}" target="_blank">View Rows</a></li>
        {% endfor %}
        </ul>
    </body>
    </html>
    """
    return HTMLResponse(content=html.replace("{% for table in tables %}", "").replace("{% endfor %}", "").replace("{{ table }}", "<br>".join(DATAFRAMES.keys())))

# Handle file upload
@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    with open(file_path, "wb") as f:
        f.write(await file.read())
    df = pd.read_excel(file_path)
    key = file.filename.lower().replace(" ", "-").replace(".xlsx", "")
    DATAFRAMES[key] = df
    return HTMLResponse(f"""
    <html>
    <head><title>Upload Successful</title><link rel="stylesheet" href="/static/style.css"></head>
    <body>
        <h2>✅ File Saved Successfully!</h2>
        <p>Table created: <b>{key}</b></p>
        <p>Your API is available at:</p>
        <code>/api/{key}</code>
        <br><br>
        <a href="/upload">Upload another file</a> | <a href="/query">Go to Query Tester</a>
    </body>
    </html>
    """)

# API endpoint for querying
@app.get("/api/{sheet_name}")
async def query_data(
    sheet_name: str,
    limit: int = 10,
    search: str = None,
    **filters,
):
    if sheet_name not in DATAFRAMES:
        return {"error": "Sheet not found. Upload first."}
    df = DATAFRAMES[sheet_name]

    # Apply filters
    for col, val in filters.items():
        if col in df.columns:
            df = df[df[col].astype(str).str.contains(str(val), case=False, na=False)]

    # Apply search across all columns
    if search:
        mask = df.apply(lambda row: row.astype(str).str.contains(search, case=False, na=False).any(), axis=1)
        df = df[mask]

    return df.head(limit).to_dict(orient="records")

# Query Tester page
@app.get("/query", response_class=HTMLResponse)
async def query_page():
    # Generate dropdown options
    options = "".join([f'<option value="/api/{t}">{t}</option>' for t in DATAFRAMES.keys()])
    html = f"""
    <html>
    <head>
        <title>Spreadsheet2API Query Tester</title>
        <link rel="stylesheet" href="/static/style.css">
    </head>
    <body>
        <h1>Spreadsheet2API Query Tester</h1>
        <label>Choose Table:</label>
        <select id="endpoint">
            {options}
        </select>
        <br><br>
        <label>Limit:
            <input type="number" id="limit" value="10">
        </label>
        <br>
        <label>Search:
            <input type="text" id="search" placeholder="Search keyword...">
        </label>
        <br>
        <label>Filter column:
            <input type="text" id="filter_col" placeholder="Column name">
        </label>
        <label>Filter value:
            <input type="text" id="filter_val" placeholder="Value">
        </label>
        <br>
        <button onclick="runQuery()">Run Query</button>
        <h2>Response:</h2>
        <pre id="output">{ "results will appear here" }</pre>

        <script>
        async function runQuery() {{
            const endpoint = document.getElementById("endpoint").value;
            const limit = document.getElementById("limit").value;
            const search = document.getElementById("search").value;
            const filterCol = document.getElementById("filter_col").value;
            const filterVal = document.getElementById("filter_val").value;

            let url = endpoint + "?limit=" + encodeURIComponent(limit);
            if (search) url += "&search=" + encodeURIComponent(search);
            if (filterCol && filterVal) url += "&" + encodeURIComponent(filterCol) + "=" + encodeURIComponent(filterVal);

            try {{
                const res = await fetch(url);
                const data = await res.json();
                document.getElementById("output").textContent = JSON.stringify(data, null, 2);
            }} catch (err) {{
                document.getElementById("output").textContent = "Error: " + err;
            }}
        }}
        </script>
    </body>
    </html>
    """
    return HTMLResponse(content=html)
