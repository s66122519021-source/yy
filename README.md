# Zoo Visitor Data Service

This FastAPI project reads the actual January fiscal year 2569 CSV resource from the same folder and returns the dataset metadata and visitor records as JSON.

## Run with PowerShell

```powershell
py -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m uvicorn main:app --reload --port 8004
```

Swagger UI is at `http://127.0.0.1:8004/docs`. Use `GET /api/zoo-visitors` to see the JSON response, including its source, fiscal year, record count, and actual CSV rows. Keep `zoo_visitors_january_2569.csv` beside `main.py`.

## Postman

Import `postman_collection.json` and send the included GET request. The collection targets `http://127.0.0.1:8004`.

Data source: https://data.go.th/dataset/zoo-visitors2569
