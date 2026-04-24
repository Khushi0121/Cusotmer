Customer Task


This project processes customer support tickets by cleaning data, classifying issues, generating insights, and exposing REST APIs using FastAPI.


pip install -r requirements.txt
uvicorn main:app --reload

Open:
http://127.0.0.1:8000/docs


* **POST /ingest** → Process `customer.csv`
* **GET /stats** → View insights (category distribution + keywords)
* **GET /search?q=...** → Search tickets
* **GET /category/{category}** → Filter by category
* **GET /summary** → Complaint summary


* Data cleaning (remove nulls, HTML, special chars)
* Rule-based classification (Complaint, Query, Request)
* Keyword extraction
* NLP-based summarization
* CSV-based storage (cleaned_customer.csv)

`customer.csv`


```bash
curl -X POST http://127.0.0.1:8000/ingest
curl http://127.0.0.1:8000/stats
